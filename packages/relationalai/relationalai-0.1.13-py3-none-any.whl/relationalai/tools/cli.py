#pyright: reportPrivateImportUsage=false
from collections import defaultdict
import io
from typing import cast, Any, List
from click.core import Context
from click.formatting import HelpFormatter
from ..clients.client import ResourceProvider
from .. import Resources
import rich
from rich.console import Console
from rich import box as rich_box
from rich.table import Table
from ..tools import debugger as deb
from ..clients import config, snowflake
from ..clients.config import (
    FIELD_PLACEHOLDER,
    ConfigFile,
    all_configs_including_legacy,
    get_from_snowflake_connections_toml,
    azure_default_props,
    snowflake_default_props,
)
from InquirerPy.base.control import Choice

import os
import sys
import click
from pathlib import Path
from .cli_controls import divider, Spinner
from . import cli_controls as controls

#--------------------------------------------------
# Constants
#--------------------------------------------------

ENGINE_SIZES = ["XS", "S", "M", "L", "XL"]
PROFILE = None

SNOWFLAKE = "Snowflake"
AZURE = "Azure (Beta)"

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def get_resource_provider(platform:str|None=None, _cfg:config.Config|None = None) -> ResourceProvider:
    cfg = _cfg or config.Config(PROFILE)
    provider = Resources(config=cfg)
    return provider

group_platforms = {
    "imports": ["snowflake"],
    "exports": ["snowflake"],
}

def group_available(group:str) -> bool:
    return group not in group_platforms \
           or config.Config(PROFILE).get("platform", "") in group_platforms[group]

def check_group(group:str):
    if not group_available(group):
        rich.print(f"[yellow]{group.capitalize()} are only available for {', '.join(group_platforms[group])}")
        divider()
        sys.exit(1)

def coming_soon():
    rich.print("[yellow]This isn't quite ready yet, but it's coming soon!")
    divider()
    sys.exit(1)

def ensure_config(profile:str|None=None) -> config.Config:
    cfg = config.Config(profile)
    if not cfg.file_path:
        rich.print("[yellow bold]No configuration file found.")
        rich.print("To create one, run: [green bold]rai init[/green bold]")
        divider()
        sys.exit(1)
    return cfg


#--------------------------------------------------
# Custom help printer
#--------------------------------------------------


class RichGroup(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        divider(console)
        console.print("[bold]Welcome to [green]RelationalAI![/bold]")
        console.print()
        console.print("rai [magenta]\\[options][/magenta] [cyan]command[/cyan]")

        console.print()
        console.print("[magenta]--profile[/magenta][dim] - which config profile to use")

        groups = defaultdict(list)
        for command in self.commands.keys():
            if ":" in command:
                group, _ = command.split(":")
                groups[group].append(command)
            else:
                groups[""].append(command)

        console.print()
        for command in groups[""]:
            console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")

        for group, commands in groups.items():
            if group:
                console.print()
                if not group_available(group):
                    plats = ", ".join(group_platforms[group])
                    console.print(f"[yellow]Only available for {plats}[/yellow]")
                for command in commands:
                    if group_available(group):
                        console.print(f"[cyan]{command}[/cyan][dim] - {self.commands[command].help}")
                    else:
                        console.print(f"[dim yellow]{command} - {self.commands[command].help}")

        divider(console)
        formatter.write(sio.getvalue())

#--------------------------------------------------
# Main group
#--------------------------------------------------

@click.group(cls=RichGroup)
@click.option("--profile", help="Which config profile to use")
def cli(profile):
    global PROFILE
    PROFILE = profile

#--------------------------------------------------
# Init
#--------------------------------------------------

@cli.command(help="Initialize a new project")
def init():
    init_flow()

#--------------------------------------------------
# Init flow
#--------------------------------------------------

def azure_flow(cfg:config.Config):
    option_selected = check_original_config_flow(cfg, "azure")
    # get the client id and secret
    client_id = controls.text("Client ID:", default=cfg.get("client_id", "") if option_selected else "")
    client_secret = controls.password("Client Secret:", default=cfg.get("client_secret", "") if option_selected else "")
    # setup the default config
    cfg.fill_in_with_azure_defaults(
        client_id=client_id,
        client_secret=client_secret
    )

def unexpand_user_path(path):
    """Inverse of os.path.expanduser"""
    home_dir = os.path.expanduser('~')
    if path.startswith(home_dir):
        return '~' + path[len(home_dir):]
    return path

def snowflake_flow(cfg:config.Config):
    option_selected:bool = False
    pyrel_config = check_original_config_flow(cfg, "snowflake")
    if pyrel_config:
        option_selected = True
    else:
        connection_selected = check_snowflake_connections_flow(cfg)
        option_selected = bool(connection_selected)
    # get account info
    user = controls.text("SnowSQL user:", default=cfg.get("user", "") if option_selected else "")
    password = controls.password("SnowSQL password:", default=cfg.get("password", "") if option_selected else "")
    account = controls.text("Snowflake account:", default=cfg.get("account", "") if option_selected else "")
    # setup the default config
    cfg.fill_in_with_snowflake_defaults(
        user=user,
        password=password,
        account=account,
    )

def filter_profiles_by_platform(config:ConfigFile, platform:str):
    filtered_config = {}
    for profile, props in config.get_combined_profiles().items():
        if profile == "__top_level__":
            continue
        if props.get("platform") == platform or (
            props.get("platform") is None
            and platform == "azure"
        ):
            filtered_config[profile] = props
    return filtered_config

def check_original_config_flow(cfg:config.Config, platform:str):
    all_profiles = {}
    for config_file in all_configs_including_legacy():
        file_path = config_file.path
        plt_config = filter_profiles_by_platform(config_file, platform)
        for profile, props in plt_config.items():
            profile_id = (profile, file_path)
            all_profiles[profile_id] = props
    if platform == "snowflake":
        sf_config = get_from_snowflake_connections_toml()
        if sf_config:
            file_path = os.path.expanduser("~/.snowflake/connections.toml")
            for profile, props in sf_config.items():
                profile_id = (profile, file_path)
                all_profiles[profile_id] = props
    if len(all_profiles) == 0:
        return
    max_profile_name_len = max(len(profile) for profile, _ in all_profiles.keys())
    profile_options: List[Choice] = []
    for profile, props in all_profiles.items():
        formatted_name = f"{profile[0]:<{max_profile_name_len}}  {unexpand_user_path(profile[1])}"
        profile_options.append(Choice(value=profile, name=formatted_name))
    selected_profile = controls.select("Use existing profile", list(profile_options), None, mandatory=False)
    if not selected_profile:
        return
    cfg.profile = selected_profile[0]
    cfg.props = all_profiles[selected_profile]
    return True

def check_snowflake_connections_flow(cfg:config.Config):
    sf_config = get_from_snowflake_connections_toml()
    if not sf_config or len(sf_config) == 0:
        return
    profiles = list(sf_config.keys())
    profile = controls.fuzzy("Use profile from ~/.snowflake/connections.toml", profiles)
    cfg.profile = profile
    cfg.props = sf_config[profile]
    return True

def spcs_flow(provider:ResourceProvider, cfg:config.Config):
    if cfg.get("platform") != "snowflake" or (cfg.get("warehouse", "") and cfg.get("rai_app_name", "")):
        return
    with Spinner("Fetching roles", "Fetched roles"):
        roles = cast(snowflake.Resources, provider).list_roles()
    role = controls.fuzzy("Select a role:", [r["name"] for r in roles], mandatory=False)
    cfg.set("role", role or FIELD_PLACEHOLDER)
    provider.reset()

    rich.print("")
    with Spinner("Fetching warehouses", "Fetched warehouses"):
        warehouses = cast(snowflake.Resources, provider).list_warehouses()
    rich.print("")
    warehouse = controls.fuzzy("Select a warehouse:", [w["name"] for w in warehouses], mandatory=False)
    cfg.set("warehouse", warehouse or FIELD_PLACEHOLDER)

    rich.print("")
    with Spinner("Fetching installed apps", "Fetched apps"):
        apps = cast(snowflake.Resources, provider).list_apps()
    rich.print("")
    app_names = [w["name"] for w in apps]
    if "relationalai" in apps:
        cfg.set("rai_app_name", "relationalai")
    else:
        app = controls.fuzzy("Select RelationalAI app name:", app_names, mandatory=False)
        cfg.set("rai_app_name", app or FIELD_PLACEHOLDER)
    provider.reset()

    rich.print("")
    with Spinner("Fetching databases", "Fetched databases"):
        databases = cast(snowflake.Resources, provider).list_databases()
    rich.print("")
    database = controls.fuzzy("Select a database:", [d["name"] for d in databases], mandatory=False)
    cfg.set("database", database or FIELD_PLACEHOLDER)

def engine_flow(provider:ResourceProvider, cfg:config.Config):
    error = False
    rich.print("")
    with Spinner("Fetching engines", "Fetched engines"):
        try:
            engines = provider.list_engines()
        except Exception as e:
            rich.print(f"[yellow]Error fetching engines: {e}")
            engines = []
            error = True

    if error:
        rich.print("")
        rich.print("[yellow]Skipping engine selection")
        cfg.set("engine", "")
        return

    engine_names = ["Create a new engine"] + [engine.get("name") for engine in engines]
    print("")
    default_engine = cfg.get("engine", "")
    if default_engine not in engine_names:
        default_engine = None
    engine = controls.fuzzy("Select an engine:", choices=engine_names, mandatory =False)
    if engine == "Create a new engine":
        engine = controls.text("Engine name:")
        engine_size = controls.fuzzy("Engine size:", choices=ENGINE_SIZES)
        engine_pool = ""
        if cfg.get("platform") == "snowflake":
            provider = cast(snowflake.Resources, provider)
            print("")
            with Spinner("Fetching compute pools", "Fetched compute pools"):
                pools = [v["name"] for v in provider.list_compute_pools()]
            print("")
            engine_pool = controls.fuzzy("Compute pool:", pools)
            cfg.set("compute_pool", engine_pool)
        rich.print("")
        with Spinner(f"Creating '{engine}' engine... (this may take several minutes)", f"Engine '{engine}' created"):
            provider.create_engine(engine, engine_size, engine_pool)
        rich.print("")
    cfg.set("engine", engine or FIELD_PLACEHOLDER)

def gitignore_flow():
    current_dir = Path.cwd()
    prev_dir = None
    while current_dir != prev_dir:
        gitignore_path = current_dir / '.gitignore'
        if gitignore_path.exists():
            # if there is, check to see if raiconfig.toml is in it
            with open(gitignore_path, 'r') as gitignore_file:
                if 'raiconfig.toml' in gitignore_file.read():
                    return
                else:
                    # if it's not, ask to add it
                    add_to_gitignore = controls.confirm("Add raiconfig.toml to .gitignore?", default=True)
                    if add_to_gitignore:
                        with open(gitignore_path, 'a') as gitignore_file:
                            gitignore_file.write("\nraiconfig.toml")
                    return
        prev_dir = current_dir
        current_dir = current_dir.parent

def save_flow(cfg:config.Config, confirmed:bool=False):
    if cfg.profile in cfg.get_profiles():
        if not controls.confirm(f"Overwrite existing {cfg.profile} profile"):
            cfg.profile = controls.text("Profile name:")
    cfg.save()

def init_flow():
    cfg = config.Config()
    #try:
    cfg.clone_profile()
    rich.print("\n[dim]---------------------------------------------------\n")
    rich.print("[bold]Welcome to [green]RelationalAI!\n")
    rich.print("Press Control-S to skip a prompt\n")
    platform = controls.fuzzy("Host platform:", choices=[SNOWFLAKE, AZURE])

    if platform == SNOWFLAKE:
        snowflake_flow(cfg)
    elif platform == AZURE:
        azure_flow(cfg)

    provider = get_resource_provider(None, cfg)

    rich.print()
    spcs_flow(provider, cfg)
    engine_flow(provider, cfg)
    save_flow(cfg)

    gitignore_flow()
    rich.print("")
    rich.print("[green]✓ raiconfig.toml saved!")
    rich.print("\n[dim]---------------------------------------------------\n")
    # except Exception as e:
    #     rich.print("")
    #     rich.print("[yellow bold]Initialization aborted!")
    #     rich.print(f"[yellow]{e}")
    #     print(e.with_traceback(None))
    #     rich.print("")

    #     save = controls.confirm("Save partial config?")
    #     if save:
    #         rich.print("")
    #         cfg.fill_in_with_defaults()
    #         save_flow(cfg)
    #         gitignore_flow()
    #         rich.print(f"[yellow bold]✓ Saved partial raiconfig.toml ({os.path.abspath('raiconfig.toml')})")

    #     divider()

#--------------------------------------------------
# Explain config
#--------------------------------------------------

@cli.command(
    name="config:explain",
    help="Inspect config status",
)
@click.option(
    "--profile",
    help="Profile to inspect",
)
@click.option(
    "--all-profiles",
    help="Whether to show all profiles in config file",
    is_flag=True,
)
def config_explain(profile:str="default", all_profiles:bool=False):
    divider()
    cfg = ensure_config(profile)

    rich.print(f"[bold green]{cfg.file_path}")
    if os.getenv("RAI_PROFILE"):
        rich.print(f"[yellow]Environment variable [bold]RAI_PROFILE = {os.getenv('RAI_PROFILE')}[/bold]")
    rich.print("")
    if cfg.profile != "__top_level__":
        rich.print(f"[bold]\\[{cfg.profile}]")

    for key, value in cfg.props.items():
        if key == "active_profile" and cfg.profile != "__top_level__":
            continue
        rich.print(f"{key} = [cyan bold]{mask(key, value)}")

    platform = cfg.get("platform", "snowflake")
    defaults = snowflake_default_props if platform == "snowflake" else azure_default_props

    for key, value in defaults.items():
        if key not in cfg.props:
            rich.print(f"[yellow bold]{key}[/yellow bold] = ?" + (
                f" (default: {value})" if value and value != FIELD_PLACEHOLDER else ""
            ))

    if all_profiles:
        for profile, props in cfg.get_profiles().items():
            if profile == cfg.profile:
                continue
            if len(props):
                rich.print()
                rich.print(f"[bold]\\[{profile}][/bold]")
                for key, value in props.items():
                    rich.print(f"{key} = [cyan bold]{mask(key, value)}")

    divider()

def mask(key: str, value: Any):
    if key in ["client_secret", "password"]:
        return str(value)[:3] + ("*" * (len(str(value)) - 3))
    return value

#--------------------------------------------------
# Check config
#--------------------------------------------------

@cli.command(
    name="config:check",
    help="Check whether config is valid",
)
def config_check(all_profiles:bool=False):
    divider()
    ensure_config()
    with Spinner("Connecting to platform..."):
        get_resource_provider().list_engines()
    rich.print("[green]✓ Connection successful!")

#--------------------------------------------------
# Debugger
#--------------------------------------------------

@cli.command(help="Open the RAI debugger")
def debugger():
    deb.main()

#--------------------------------------------------
# Engine list
#--------------------------------------------------

@cli.command(name="engines:list", help="List all engines")
def engines_list():
    divider(flush=True)
    ensure_config()
    with Spinner("Fetching engines"):
        engines = get_resource_provider().list_engines()

    if len(engines):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Name")
        table.add_column("Size")
        table.add_column("State")
        for engine in engines:
            table.add_row(engine.get("name"), engine.get("size"), engine.get("state"))
        rich.print(table)
    else:
        rich.print("[yellow]No engines found")

    divider()

#--------------------------------------------------
# Engine create
#--------------------------------------------------

@cli.command(name="engines:create", help="Create a new engine")
@click.option("--name", help="Name of the engine")
@click.option("--size", type=click.Choice(ENGINE_SIZES, case_sensitive=False), help="Size of the engine")
def engines_create(name, size):
    divider(flush=True)
    ensure_config()
    name = controls.prompt("Engine name?", name, newline=True)
    if not size:
        size = controls.fuzzy("Engine size:", choices=ENGINE_SIZES)
        rich.print("")
    provider = get_resource_provider()

    pool = provider.config.get("compute_pool", None, strict=False)
    if provider.config.get("platform") == "snowflake" and not pool:
        provider = cast(snowflake.Resources, provider)
        rich.print("")
        with Spinner("Fetching compute pools", "Fetched compute pools"):
            pools = [v["name"] for v in provider.list_compute_pools()]
        rich.print("")
        pool = controls.fuzzy("Compute pool:", pools)
        rich.print("")

    with Spinner(f"Creating '{name}' engine... (this may take several minutes)", f"Engine '{name}' created!"):
        provider.create_engine(name, size, pool)
    divider()

#--------------------------------------------------
# Engine delete
#--------------------------------------------------

@cli.command(name="engines:delete", help="Delete an engine")
@click.option("--name", help="Name of the engine")
def engines_delete(name):
    divider(flush=True)
    ensure_config()
    if not name:
        with Spinner("Fetching engines"):
            engines = get_resource_provider().list_engines()
        name = controls.fuzzy("Select an engine:", [engine["name"] for engine in engines])
        print("")

    with Spinner(f"Deleting '{name}' engine", f"Engine '{name}' deleted!"):
        get_resource_provider().delete_engine(name)
    divider()

#--------------------------------------------------
# Object flow
#--------------------------------------------------

def object_flow(provider):
    with Spinner("Fetching databases", "Databases fetched"):
        dbs = provider.list_databases()
    rich.print()
    db = controls.fuzzy("Select a database:", [db["name"] for db in dbs])
    rich.print()

    with Spinner("Fetching schemas", "Schemas fetched"):
        schemas = provider.list_sf_schemas(db)
    rich.print()
    schema = controls.fuzzy("Select a schema:", [s["name"] for s in schemas])
    rich.print()

    with Spinner("Fetching tables", "Tables fetched"):
        tables = provider.list_tables(db, schema)
    rich.print()
    table = controls.fuzzy("Select tables (tab for multiple):", [t["name"] for t in tables], multiselect=True)
    rich.print()
    return db, schema, table

#--------------------------------------------------
# Imports list
#--------------------------------------------------

@cli.command(name="imports:list", help="List objects imported into RAI")
@click.option("--model", help="Model")
def imports_list(model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        imports = provider.list_imports(model)

    rich.print()
    if len(imports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Import")
        for imp in imports:
            table.add_row(imp.get("name"))
        rich.print(table)
    else:
        rich.print("[yellow]No imports found")

    divider()

#--------------------------------------------------
# Imports stream
#--------------------------------------------------

@cli.command(name="imports:stream", help="Stream an object into RAI")
@click.option("--object", help="Object")
@click.option("--model", help="Model")
@click.option("--rate", help="Rate")
def imports_stream(object, model, rate):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    if not object:
        db, schema, table = object_flow(provider)
        for t in table:
            obj = f"{db}.{schema}.{t}"
            with Spinner(f"Creating stream for {obj}", f"Stream for {obj} created"):
                provider.create_import_stream(obj, model, rate)
    else:
        with Spinner(f"Creating stream for {object}", f"Stream for {object} created"):
            provider.create_import_stream(object, model, rate)

    divider()

#--------------------------------------------------
# Imports delete
#--------------------------------------------------

@cli.command(name="imports:delete", help="Delete an import from RAI")
@click.option("--object", help="Object")
@click.option("--model", help="Model")
def imports_delete(object, model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    check_group("imports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching imports for {model}", "Imports fetched"):
        imports = provider.list_imports(model)

    if not imports:
        rich.print()
        rich.print("[yellow]No imports to delete")
    elif not object:
        rich.print()
        objects = controls.fuzzy("Select objects (tab for multiple):", [t["name"] for t in imports], multiselect=True)
        rich.print()
        for object in objects:
            with Spinner(f"Removing {object}", f"{object} removed"):
                provider.delete_import(object, model)
    else:
        with Spinner(f"Removing {object}", f"{object} removed"):
            provider.delete_import(object, model)

    divider()

#--------------------------------------------------
# Exports list
#--------------------------------------------------

@cli.command(name="exports:list", help="List objects exported out of RAI")
@click.option("--model", help="Model")
def exports_list(model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()
    check_group("exports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    with Spinner(f"Fetching exports for {model}", "Exports fetched"):
        exports = provider.list_exports(model, "")

    rich.print()
    if len(exports):
        table = Table(show_header=True, border_style="dim", header_style="bold", box=rich_box.SIMPLE_HEAD)
        table.add_column("Object")
        for imp in exports:
            table.add_row(imp.get("name"))
        rich.print(table)
    else:
        rich.print("[yellow]No exports found")

    divider()

#--------------------------------------------------
# Exports delete
#--------------------------------------------------

@cli.command(name="exports:delete", help="Delete an export from RAI")
@click.option("--export", help="export")
@click.option("--model", help="Model")
def exports_delete(export, model):
    divider(flush=True)
    ensure_config()
    provider = cast(snowflake.Resources, get_resource_provider())
    coming_soon()
    check_group("exports")

    if not model:
        with Spinner("Fetching models", "Models fetched"):
            models = provider.list_graphs()
        rich.print()
        model = controls.fuzzy("Select a model:", models)
        rich.print()

    if not export:
        db, schema, table = object_flow(provider)
        for t in table:
            export = f"{db}.{schema}.{t}"
            with Spinner(f"Removing {export}", f"{export} removed"):
                provider.delete_export(model, "", export)
    else:
        with Spinner(f"Removing {export}", f"{export} removed"):
            provider.delete_export(model, "", export)

    divider()

#--------------------------------------------------
# Main
#--------------------------------------------------

if __name__ == "__main__":
    # app = EventApp()
    # app.run()
    cli()
