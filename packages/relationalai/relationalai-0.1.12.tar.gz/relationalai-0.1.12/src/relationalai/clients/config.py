import os
from typing import Dict, Any
from railib import config
import configparser
import toml
import tomlkit


#--------------------------------------------------
# config defaults
#--------------------------------------------------

FIELD_PLACEHOLDER = ""

snowflake_default_props = {
    "platform": "snowflake",
    "user": FIELD_PLACEHOLDER,
    "password": FIELD_PLACEHOLDER,
    "account": FIELD_PLACEHOLDER,
    "role": "PUBLIC",
    "warehouse": FIELD_PLACEHOLDER,
    "database": FIELD_PLACEHOLDER,
    "rai_app_name": FIELD_PLACEHOLDER,
    "engine": FIELD_PLACEHOLDER,
    "compute_pool": FIELD_PLACEHOLDER,
}

azure_default_props = {
    "platform": "azure",
    "host": "azure.relationalai.com",
    "port": 443,
    "region": "us-east",
    "scheme": "https",
    "client_credentials_url": "https://login.relationalai.com/oauth/token",
    "client_id": FIELD_PLACEHOLDER,
    "client_secret": FIELD_PLACEHOLDER,
}

#--------------------------------------------------
# helpers
#--------------------------------------------------

class ConfigFile:
    def __init__(
        self,
        path: str | None = None,
        cfg: Dict[str, Any] = {},
        *,
        format = "toml"
    ):
        if format == "toml":
            self.path:str|None = path
            self.profiles:Dict[str,Dict[str,Any]] = cfg.get("profile", {})
            self.config:Dict[str,Any] = {}
            for key in cfg:
                if key != "profile":
                    self.config[key] = cfg[key]
        elif format == "ini":
            self.path = path
            self.profiles = {
                k: {k2: v2 for k2, v2 in v.items()}
                for k, v in cfg.items()
                if k != "DEFAULT"
            }
            self.config = {}
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def apply_keymap(self):
        keymap = {
            "snowsql_user": "user",
            "snowsql_pwd": "password",
        }
        for key in self.config.copy():
            self.config[keymap.get(key, key)] = self.config[key]
        for profile, props in self.profiles.copy().items():
            for key in props.copy():
                self.profiles[profile][keymap.get(key, key)] = props[key]

    def get_combined_profiles(self):
        combined_profiles = {}
        combined_profiles["__top_level__"] = self.config or {}
        for profile in self.profiles:
            combined_profiles[profile] = self.profiles[profile].copy()
        return combined_profiles
    
    def map(self, f):
        """
        Apply a function `f` to all props dictionaries in the configuration files, including the top-level dictionary and all profiles.
        """
        combined_profiles = self.get_combined_profiles()
        for profile in combined_profiles:
            combined_profiles[profile] = f(combined_profiles[profile])
        config = combined_profiles.pop("__top_level__")
        return self.__class__(
            self.path, { **config, "profile": combined_profiles }
        )

    def filled_from_snowflake_connection(self):
        def fill(props):
            if "snowflake-connection" in props:
                connection_name = props.pop("snowflake-connection")
                snowflake_config = get_from_snowflake_connections_toml()
                if snowflake_config and connection_name in snowflake_config:
                    return {
                        **snowflake_config[connection_name],
                        **props,
                    }
            return props
        return self.map(fill)

    def merge(self, other):
        """
        Merge the profiles from `other` into this ConfigFile object
        """
        combined_profiles = self.get_combined_profiles()
        other_combined_profiles = other.get_combined_profiles()

        all_profile_names = set(combined_profiles) | set(other_combined_profiles)

        for profile in all_profile_names:
            self_profile = combined_profiles.get(profile, {})
            other_profile = other_combined_profiles.get(profile, {})
            combined_profiles[profile] = {**other_profile, **self_profile}

        config = combined_profiles.pop("__top_level__", None)

        if config is not None:
            self.config = config
        self.profiles = combined_profiles


def first(x):
    return next(iter(x), None)

def _search_upwards_for_file(file:str):
    """
    Search for `file` in the current directory and all parent directories.

    Returns the absolute path to the file if found, otherwise None.
    """
    dir = os.path.abspath(os.getcwd())
    while True:
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            yield file_path
        parent_dir = os.path.dirname(dir)
        if parent_dir == dir:
            break # reached the root
        dir = parent_dir

def _search_userdir_for_file(file:str):
    """
    Search for `file` in the user's home directory.

    Returns the absolute path to the file if found, otherwise None.
    """
    file_path = os.path.expanduser(f"~/{file}")
    if os.path.isfile(file_path):
        yield file_path

def _find_config_file():
    yield from _search_upwards_for_file("raiconfig.toml")
    yield from _search_userdir_for_file(".rai/raiconfig.toml")

def _parse_and_map_config(file:str):
    """
    Parse the config file at `file` and return a dictionary of config values.

    Handles both TOML and INI files.

    The legacy keys "snowsql_user" and "snowsql_pwd" are mapped to "user" and "password"
    """
    if not os.path.exists(file):
        return ConfigFile(cfg={})
    if file.endswith(".toml"):
        try:
            return ConfigFile(file, toml.load(file))
        except toml.TomlDecodeError as e:
            raise Exception(f"Error parsing {file}: {e}")
    config = configparser.ConfigParser()
    config.read(file)
    cf = ConfigFile(file, {k: v for k, v in config.items() if k != "DEFAULT"}, format="ini")
    cf.apply_keymap()
    return cf

def _get_full_config(profile:str|None=None) -> tuple[Dict[str,Any], str|None]:
    """
    Returns a dictionary representing the props to be used for the currently active profile. Incorporates the following rules:
    1. The `snowflake-connection` key fills in the properties from the Snowflake connections.toml file.
    2. Profiles with the same name are merged in order of appearance, with earlier profiles taking precedence.
    3. The profile indicated by the `active-profile` key is merged into other top-level properties.
    """
    files = list(_find_config_file())
    file_path = first(files)
    if not files:
        return {}, file_path
    config_files = [
        _parse_and_map_config(file).filled_from_snowflake_connection()
        for file in files
    ]
    for i in range(len(config_files) - 1, 0, -1):
        config_files[i-1].merge(config_files[i])
    if not config_files:
        return {}, file_path
    root_file = config_files[0]
    if profile:
        root_file.config["active-profile"] = profile
    if ("active-profile" in root_file.config and
        root_file.config["active-profile"] in root_file.profiles):
        active_profile = root_file.config["active-profile"]
        config = {
            **root_file.profiles[active_profile],
            **root_file.config,
        }
    else:
        config = root_file.config
    return config, file_path

def has_platform(cfg, platform):
    return any(profile.get("platform") == platform for profile in cfg.get_combined_profiles().values())

def _legacy_config_files():
    """
    Generates all legacy config files found

    Includes both ~/.rai/config and rai.config (in a parent directory
    or the user's home directory)
    """
    yield from _search_upwards_for_file("rai.config")
    yield from _search_userdir_for_file(".rai.config")
    path = os.path.expanduser("~/.rai/config")
    if os.path.exists(path):
        yield path

def legacy_config_exists():
    return any(_legacy_config_files())

def all_configs_including_legacy():
    for file in _find_config_file():
        yield _parse_and_map_config(file)
    for file in _legacy_config_files():
        yield _parse_and_map_config(file)

def get_from_snowflake_connections_toml():
    user_config_path = os.path.expanduser("~/.snowflake/connections.toml")
    if os.path.exists(user_config_path):
        try:
            snow_config = toml.load(user_config_path)
        except toml.TomlDecodeError as e:
            raise Exception(f"Error parsing {user_config_path}: {e}")
        config = {}
        for profile in snow_config:
            config[profile] = {}
            for key in snow_config[profile]:
                config[profile][key] = snow_config[profile][key]
        return config

def to_rai_config(data:Dict[str, Any]) -> Dict[str, Any]:
    creds = config._read_client_credentials(data)
    _keys = ["host", "port", "region", "scheme", "audience"]
    result = {k: v for k, v in data.items() if k in _keys}
    result["credentials"] = creds
    return result

#--------------------------------------------------
# Config
#--------------------------------------------------

class Config():
    def __init__(self, profile:str|Dict[str,Any]|None=None):
        supplied_props = None
        if isinstance(profile, dict):
            supplied_props = profile
            profile = "__top_level__"
        self.fetch(profile)
        self.cache_config_file_contents()
        if supplied_props is not None:
            for k, v in supplied_props.items():
                self.set(k, v)
            if not self.file_path:
                self.file_path = "__inline__"

    def get_profiles(self):
        if not self.original_toml:
            return {}
        return self.original_toml.get("profile", {})

    def fetch(self, profile:str|None=None):
        cfg, path = _get_full_config(profile)
        self.file_path = path
        self.profile = (
            profile or
            cfg.get("active-profile", None) or
            os.environ.get("RAI_PROFILE", "__top_level__")
        )
        self.props = cfg

    def cache_config_file_contents(self):
        self.original_toml = tomlkit.document()
        if self.file_path is None:
            return
        with open(self.file_path, "r") as f:
            try:
                self.original_toml = tomlkit.parse(f.read())
            except toml.TomlDecodeError as e:
                raise Exception(f"Error parsing {self.file_path}: {e}")
        return

    def clone_profile(self):
        self.props = {k: v for k,v in self.props.items()}

    def get(self, name:str, default:Any|None=None, strict:bool=True):
        val = self.props.get(name, os.environ.get(name, default))
        if val is None and strict:
            raise Exception(f"Missing config value for '{name}'")
        return val

    def set(self, name:str, value:str|int):
        self.props[name] = value

    def unset(self, name:str):
        del self.props[name]

    def to_rai_config(self) -> Dict[str, Any]:
        return to_rai_config(self.props)

    def save(self):
        new_document = tomlkit.document()
        if self.profile != "__top_level__":
            active_profile = self.profile
        else:
            active_profile = self.get("active-profile", None, strict=False)
        if active_profile is not None:
            new_document["active-profile"] = active_profile
            new_document.add(tomlkit.nl())
        if self.profile == "__top_level__":
            for k, v in self.props.items():
                new_document[k] = v
        for key, value in self.original_toml.items():
            if key not in new_document:
                new_document[key] = value
        if self.profile != "__top_level__":
            profiles = new_document.get("profile", tomlkit.table())
            if self.profile not in profiles:
                profiles[self.profile] = tomlkit.table()
            profile_table = profiles[self.profile]
            for k, v in self.props.items():
                profile_table[k] = v
            new_document["profile"] = profiles
        with open("raiconfig.toml", "w") as f:
            f.write(tomlkit.dumps(new_document))

    def _fill_in_with_defaults(self, defaults: Dict[str, Any], **kwargs):
        props = {k: v for k, v in kwargs.items() if k in defaults}
        self.props = {
            **defaults,
            **self.props,
            **props,
        }

    def fill_in_with_azure_defaults(self, **kwargs):
        self._fill_in_with_defaults(azure_default_props, **kwargs)

    def fill_in_with_snowflake_defaults(self, **kwargs):
        self._fill_in_with_defaults(snowflake_default_props, **kwargs)

    def fill_in_with_defaults(self):
        platform = self.get("platform", None, strict=False)
        if platform == "azure":
            self.fill_in_with_azure_defaults()
        elif platform == "snowflake":
            self.fill_in_with_snowflake_defaults()
        else:
            self.set("platform", "snowflake")
            self.fill_in_with_snowflake_defaults()