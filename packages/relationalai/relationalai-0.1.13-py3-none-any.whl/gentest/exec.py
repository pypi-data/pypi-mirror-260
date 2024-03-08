from contextlib import contextmanager
from pathlib import Path

from relationalai.clients.test import Document, Query
from relationalai import clients
from gentest.util import PROJECT_DIR
from gentest.validate.roundtrip import exec_and_run_callback

AzureClient = clients.azure.Client
SnowflakeClient = clients.snowflake.Client
AzureProxyClient = clients.test.proxy_client(AzureClient)
SnowflakeProxyClient = clients.test.proxy_client(SnowflakeClient)

@contextmanager
def proxy_clients():
    try:
        clients.azure.Client = AzureProxyClient
        clients.snowflake.Client = SnowflakeProxyClient
        yield
    finally:
        clients.azure.Client = AzureClient
        clients.snowflake.Client = SnowflakeProxyClient


def path_to_slug(path: Path, base_path:str|Path = PROJECT_DIR):
    return str(path.relative_to(base_path)).replace("/", "__").replace(".py", "")

def validate_query_results(file_path: Path, snapshot):
    with open(file_path, "r") as file:
        code = file.read()
        with proxy_clients():
            # @TODO: Consider suppressing stdout
            doc: Document = exec_and_run_callback(code)
            for block in doc.blocks:
                if isinstance(block, Query):
                    snapshot.assert_match(str(block.result), f"query{block.ix}.txt")
