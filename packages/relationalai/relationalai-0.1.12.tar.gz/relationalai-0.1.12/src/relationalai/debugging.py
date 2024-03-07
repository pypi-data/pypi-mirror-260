import ast
from dataclasses import dataclass
import inspect
import json
from textwrap import dedent
import os
from typing import Dict
import logging

from pandas import DataFrame
from .errors import Errors
from .metamodel import Action, Task

DEBUG = True

#--------------------------------------------------
# Logging
#--------------------------------------------------

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(record.msg)

class FlushingFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

with open('debug.jsonl', 'w'):
    pass

logger = logging.getLogger("pyrellogger")
logger.setLevel(logging.DEBUG)
file_handler = FlushingFileHandler('debug.jsonl', mode='a')
file_handler.setFormatter(JsonFormatter())
logger.addHandler(file_handler)
logger.propagate = False

def time(type:str, elapsed:float, results:DataFrame = DataFrame(), **kwargs):
    if DEBUG:
        d = {"event":"time",
             "type": type,
             "elapsed": elapsed,
             "results": {"values": results.head(20).to_json(orient="records"),
                          "count": len(results)}
            }
        d.update(kwargs)
        logger.debug(d)

def handle_compilation(compilation):
    if DEBUG:
        passes = [{"name": p[0], "task": str(p[1]), "elapsed": p[2]} for p in compilation.passes]
        (file, line, block) = compilation.get_source()
        emitted = compilation.emitted
        if isinstance(emitted, list):
            emitted = "\n\n".join(emitted)
        logger.debug({
            "event":"compilation",
            "source": {"file": file, "line": line, "block": block},
            "task": str(compilation.task),
            "passes": passes,
            "emitted": emitted,
            "emit_time": compilation.emit_time
        })

#--------------------------------------------------
# SourceInfo
#--------------------------------------------------

@dataclass
class SourceInfo:
    file: str = "Unknown"
    line: int = 0
    source: str = ""
    block: ast.AST|None = None

    def modify(self, transformer:ast.NodeTransformer):
        if not self.block:
            raise Exception("Cannot modify source info without a block")

        new_block = transformer.visit(self.block)
        return SourceInfo(self.file, self.line, ast.unparse(new_block), new_block)

#--------------------------------------------------
# Jupyter
#--------------------------------------------------

class Jupyter:
    def __init__(self):
        self.dirty_cells = set()
        try:
            from IPython import get_ipython # type: ignore
            self.ipython = get_ipython()
            if self.ipython:
                self.ipython.events.register('pre_run_cell', self.pre_run_cell)
                self.dirty_cells.add(self.cell())
        except ImportError:
            self.ipython = None

    def pre_run_cell(self, info):
        self.dirty_cells.add(info.cell_id)

    def cell_content(self):
        if self.ipython:
            last_input = self.ipython.user_ns['In'][-1]
            return (last_input, f"In[{len(self.ipython.user_ns['In'])}]")
        return ("", "")

    def is_colab(self):
        if not self.ipython:
            return False
        try:
            parent = self.ipython.get_parent() #type: ignore
        except Exception:
            return False
        if not parent or "metadata" not in parent:
            return False
        return "colab" in parent["metadata"]

    def cell(self):
        if self.ipython:
            if self.is_colab():
                return self.ipython.get_parent()["metadata"]["colab"]["cell_id"] #type: ignore
            else:
                try:
                    return self.ipython.get_parent()["metadata"]["cellId"] #type: ignore
                except KeyError:
                    return None
        return None

jupyter = Jupyter()

#--------------------------------------------------
# Position capture
#--------------------------------------------------

def first_non_relationalai_frame(frame):
    while frame and frame.f_back:
        file = frame.f_code.co_filename
        if "site-packages/relationalai" not in file and "src/relationalai" not in file:
            break
        frame = frame.f_back
    return frame

def capture_code_info(steps=None):
    # Get the current frame and go back to the caller's frame
    caller_frame = inspect.currentframe()
    if steps is not None:
        for _ in range(steps):
            if not caller_frame or not caller_frame.f_back:
                break
            caller_frame = caller_frame.f_back
    else:
        caller_frame = first_non_relationalai_frame(caller_frame)

    if not caller_frame:
        return

    caller_filename = caller_frame.f_code.co_filename
    caller_line = caller_frame.f_lineno

    relative_filename = os.path.relpath(caller_filename, os.getcwd())

    # Read the source code from the caller's file
    source_code = None
    try:
        with open(caller_filename, "r") as f:
            source_code = f.read()
    except IOError:
        (jupyter_code, jupyter_cell) = jupyter.cell_content()
        if jupyter_code:
            source_code = jupyter_code
            relative_filename = jupyter_cell

    if not source_code:
        return SourceInfo(relative_filename, caller_line)

    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Find the node that corresponds to the call
    class BlockFinder(ast.NodeVisitor):
        def __init__(self, target_lineno):
            self.target_lineno = target_lineno
            self.block_node = None

        def generic_visit(self, node):
            if hasattr(node, "lineno") and node.lineno == self.target_lineno:
                self.block_node = node
                # Stop visiting once the target node is found
                return
            ast.NodeVisitor.generic_visit(self, node)

    finder = BlockFinder(caller_line)
    finder.visit(tree)

    if finder.block_node:
        # Extract the lines from the source code
        start_line = finder.block_node.lineno
        end_line = getattr(finder.block_node, "end_lineno", start_line)

        block_lines = source_code.splitlines()[start_line - 1:end_line]
        block_code = "\n".join(block_lines)
        return SourceInfo(relative_filename, caller_line, dedent(block_code), finder.block_node)

    lines = source_code.splitlines()
    if caller_line > len(lines):
        return SourceInfo(relative_filename, caller_line)
    return SourceInfo(relative_filename, caller_line, lines[caller_line - 1])

def check_errors(task:Task|Action):
    class ErrorFinder(ast.NodeVisitor):
        def __init__(self, start_line):
            self.errors = []
            self.start_line = start_line

        def to_line_numbers(self, node):
            return (node.lineno, node.end_lineno)

        def generic_visit(self, node):
            if isinstance(node, ast.If):
                Errors.invalid_if(task, *self.to_line_numbers(node))
            elif isinstance(node, ast.For) or isinstance(node, ast.While):
                Errors.invalid_loop(task, *self.to_line_numbers(node))
            elif isinstance(node, ast.Try):
                Errors.invalid_try(task, *self.to_line_numbers(node))

            ast.NodeVisitor.generic_visit(self, node)

    source = get_source(task)
    if not source or not source.block:
        return
    ErrorFinder(source.line).visit(source.block)


sources:Dict[Task|Action, SourceInfo|None] = {}
def set_source(item, steps=1, dynamic=False):
    found = capture_code_info(steps + 2)
    if found:
        sources[item] = found
        if not dynamic:
            check_errors(item)
            pass
    return found

def get_source(item):
    return sources.get(item)
