from .clients import config as cfg
from . import clients
from . import dsl
from . import debugging
from . import metamodel
from . import rel
from .loaders import csv
from . import analysis
from . import tools

def Model(name:str, *, profile:str|None=None, config:cfg.Config|None=None, dry_run:bool=False):
    config = config or cfg.Config(profile=profile)
    if not config.file_path:
        if cfg.legacy_config_exists():
            message = (
                "Use `rai init` to migrate your configuration file "
                "to the new format (raiconfig.toml)"
            )
        else:
            message = "No configuration file found. Please run `rai init` to create one."
        raise Exception(message)
    if config.get("platform") is None:
        config.set("platform", "snowflake")
    platform = config.get("platform")
    if platform == "azure":
        return clients.azure.Graph(
            name, profile=profile, config=config, dry_run=dry_run
        )
    elif platform == "snowflake":
        return clients.snowflake.Graph(
            name, profile=profile, config=config, dry_run=dry_run
        )
    else:
        raise Exception(f"Unknown platform: {platform}")

def Resources(profile:str|None=None, config:cfg.Config|None=None):
    config = config or cfg.Config(profile)
    platform = config.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Resources(config=config)
    elif platform == "snowflake":
        return clients.snowflake.Resources(config=config)
    else:
        raise Exception(f"Unknown platform: {platform}")

def Graph(name:str, dry_run:bool=False):
    return Model(name, profile=None, dry_run=dry_run)

__all__ = ['Model', 'Resources', 'dsl', 'rel', 'debugging', 'metamodel', 'csv', 'analysis', 'tools']