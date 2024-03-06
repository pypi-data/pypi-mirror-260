from .clients import config
from . import clients
from . import dsl
from . import debugging
from . import metamodel
from . import rel
from .loaders import csv
from . import analysis
from . import tools

def Model(name:str, dry_run:bool=False):
    cfg = config.Config()
    if not cfg.file_path:
        raise Exception("No configuration file found. Please run `rai init` to create one.")
    platform = cfg.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Graph(name, dry_run)
    elif platform == "snowflake":
        return clients.snowflake.Graph(name, dry_run)
    else:
        raise Exception(f"Unknown platform: {platform}")

def Resources(profile:str|None=None, cfg:config.Config|None=None):
    cfg = cfg or config.Config(profile)
    platform = cfg.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Resources(config=cfg)
    elif platform == "snowflake":
        return clients.snowflake.Resources(config=cfg)
    else:
        raise Exception(f"Unknown platform: {platform}")

__all__ = ['Model', 'Resources', 'dsl', 'rel', 'debugging', 'metamodel', 'csv', 'analysis', 'tools']