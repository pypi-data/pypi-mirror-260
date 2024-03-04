from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, cast

from pandas import DataFrame
from ..clients.client import Client
from .. import debugging
from .. import dsl, rel, metamodel as m

@dataclass
class Query:
    task: m.Task
    ix: int
    code: str|None = None
    err: Exception|None = None
    result: Any = None


@dataclass
class Install:
    task: m.Task
    name: str|None = None
    code: str|None = None
    err: Exception|None = None


class Document():
    blocks: list[Query | Install]
    query_count: int

    def __init__(self):
        self.blocks = []
        self.query_count = 0

    def __str__(self):
        parts = []
        h = "==[ Document ]"
        print(f"{h}{'='*(80 - len(h))}")
        for block in self.blocks:
            match block:
                case Query():
                    h = f"----[ Query {block.ix} ]"
                    parts.append(f"{h}{'-'*(80 - len(h))}")
                    parts.append(str(block.task))
                case Install():
                    h = f"----[ Rule {block.name} ]"
                    parts.append(f"{h}{'-'*(80 - len(h))}")
                    parts.append(str(block.task))

        return "\n".join(parts)


class NoopClient():
    def __init__(self, *_args, **_kwargs):
        self.compiler = rel.Compiler()

    def query(self, task: m.Task, *args, **kwargs):
        self.compiler.compile(task)
        return DataFrame()

    def install(self, name: str, task: m.Task, *args, **kwargs):
        self.compiler.compile(task)

    def export_udf(self, name, inputs, out_fields, task):
        pass

    def exec_raw(self, raw_code:str):
        raise Exception("Cannot exec raw code in test executor")

    def load_raw_file(self, path:str):
        raise Exception("Cannot load raw file in test executor")

proxied_clients: list[Document] = []


def proxy_client(client_class, throw_on_error = True):
    class ProxiedClient(client_class, Document):
        def __init__(self, *args, throw_on_error = True, **kwargs):
            self.blocks: list[Query | Install] = []
            self.query_count = 0
            self.throw_on_error = throw_on_error
            self.resources = {}
            # self.capture_handler = CaptureHandler()

            # debugging.logger.addHandler(self.capture_handler)
            super().__init__(*args, **kwargs)
            proxied_clients.append(self)

        # def __del__(self):
        #     # @FIXME: This is apparently not reliable
        #     debugging.logger.removeHandler(self.capture_handler)

        @contextmanager
        def capture_debugging(self):
            orig_logger_debug = debugging.logger.debug
            msgs = []
            def capture(msg):
                msgs.append(msg)
                orig_logger_debug(msg)

            setattr(debugging.logger, "debug", capture)
            try:
                yield msgs
            finally:
                setattr(debugging.logger, "debug", orig_logger_debug)

        def get_emitted(self, msgs: list):
            msgs[0]["emitted"] if len(msgs) > 0 and msgs[0]["event"] == "compilation" else None

        def query(self, task:m.Task, *args, **kwargs):
            ix = self.query_count
            self.query_count += 1
            res = None
            with self.capture_debugging() as msgs:
                try:
                    res = super().query(task, *args, **kwargs)
                    self.blocks.append(Query(task, ix, self.get_emitted(msgs), None, res))

                except Exception as err:
                    self.blocks.append(Query(task, ix, self.get_emitted(msgs), err))
                    if self.throw_on_error:
                        raise

            return res

        def install(self, name, task:m.Task, *args, **kwargs):
            with self.capture_debugging() as msgs:
                try:
                    super().install(name, task, *args, **kwargs)
                    self.blocks.append(Install(task, name, self.get_emitted(msgs)))
                except Exception as err:
                    self.blocks.append(Install(task, name, self.get_emitted(msgs), err))
                    if self.throw_on_error:
                        raise

    return ProxiedClient

Executor = proxy_client(NoopClient, throw_on_error=False)

def Graph(name, engine:str|None=None, dry_run=False):
    client = cast(Client, Executor(name, engine, dry_run))
    return dsl.Graph(client, name)
