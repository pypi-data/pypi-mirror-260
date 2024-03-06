import os
from typing import Dict, Any
from railib import config
import configparser

#--------------------------------------------------
# helpers
#--------------------------------------------------

def _find_config_file():
    dir = os.path.abspath(os.getcwd())
    # Look in the current directory and all parent directories for a rai.config file:
    while True:
        file_path = os.path.join(dir, "rai.config")
        if os.path.isfile(file_path):
            return file_path
        parent_dir = os.path.dirname(dir)
        if parent_dir == dir:
            break # reached the root
        dir = parent_dir
    if os.path.exists(os.path.expanduser("~/.rai.config")):
        return os.path.expanduser("~/.rai.config")

def _get_config(file:str|None=None):
    if not file:
        file = _find_config_file()
    if not file:
        return {}
    config = configparser.ConfigParser()
    config.read(file)
    cfg = {}
    for key, value in config.items():
        cfg[key] = {k: v for k,v in value.items()}
    return cfg

def to_rai_config(data:Dict[str, Any]) -> Dict[str, Any]:
    creds = config._read_client_credentials(data)
    _keys = ["host", "port", "region", "scheme", "audience"]
    result = {k: v for k, v in data.items() if k in _keys}
    result["credentials"] = creds
    return result

snowflake_default_props = {
    "platform": "snowflake",
    "snowsql_user": "username_here",
    "snowsql_pwd": "password_here",
    "account": "account_here",
    "role": "role_here",
}

azure_default_props = {
    "platform": "azure",
    "host": "azure.relationalai.com",
    "port": 443,
    "region": "us-east",
    "scheme": "https",
    "client_id": "client_id_here",
    "client_secret": "client_secret_here",
}

#--------------------------------------------------
# Config
#--------------------------------------------------

class Config():
    def __init__(self, profile:str|None=None):
        self.profile:str = profile or os.environ.get("RAI_PROFILE", "default")
        self.file_path = None
        self.fetch()

    def get_profiles(self):
        return self.profiles.keys()

    def fetch(self):
        config_file = _find_config_file()
        if config_file:
            self.file_path = os.path.abspath(config_file)
        self.profiles = _get_config(config_file)
        self.props = self.profiles.get(self.profile, {})

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
        self.profiles[self.profile] = self.props
        # save the config in ini format in rai.config
        with open("rai.config", "w") as f:
            for profile, props in self.profiles.items():
                if len(props):
                    f.write(f"[{profile}]\n")
                    for key, value in props.items():
                        f.write(f"{key} = {str(value).replace('%', '%%')}\n")
                    f.write("\n")

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