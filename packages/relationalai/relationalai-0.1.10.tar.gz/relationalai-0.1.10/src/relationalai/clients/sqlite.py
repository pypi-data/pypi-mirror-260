from collections import defaultdict
import numbers
import textwrap
from typing import Any, cast
from pandas import read_sql_query
from .. import dsl, rel, metamodel as m, compiler as c, debugging
import sqlean as sqlite3
import time

# Pandas warns us about sqlean not being the right adapter, but it's just
# sqlite3, so we can ignore it.
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

#--------------------------------------------------
# Emitter
#--------------------------------------------------

sql_filter = [">", "<", ">=", "<=", "=", "!="]
sql_infix = ["+", "-", "*", "/"]

class Emitter(c.Emitter):
    def __init__(self):
        super().__init__()
        self.namer = m.Namer()
        self.existing_binds = defaultdict(list)

    #--------------------------------------------------
    # Emit
    #--------------------------------------------------

    def emit(self, task: m.Task):
        self.namer.reset()
        statements = self.emit_task(task)
        if isinstance(statements, str):
            return [statements]
        return [*flatten(statements)]

    def emit_task(self, task: m.Task):
        try:
            return getattr(self, task.behavior.value)(task)
        except Exception as e:
            print("EMIT FAILED:", e)
            raise e

    #--------------------------------------------------
    # Var
    #--------------------------------------------------

    def emit_var(self, var: m.Var, sources: dict):
        val = var.value if isinstance(var, m.Var) else var
        if isinstance(val, str):
            return f"'{val}'"
        elif isinstance(val, numbers.Number):
            return f"{val}"
        return sources.get(var, "??")

    #--------------------------------------------------
    # Sequence
    #--------------------------------------------------

    def sequence_action(self, action: m.Action):
        if action.entity.value == m.Builtins.RawCode:
            return [*action.bindings.values()][0].value
        elif isinstance(action.entity.value, m.Task):
            return self.emit_task(action.entity.value)
        else:
            raise Exception("Unsupported sequence action: " + str(action))

    def sequence(self, task: m.Task):
        items = [ self.sequence_action(i) for i in task.items ]
        return items

    #--------------------------------------------------
    # Query
    #--------------------------------------------------

    def query(self, task: m.Task):
        pre = []
        view = ""
        bind = None
        selects = []
        froms = []
        wheres = []
        raws = []
        sources = {}
        for item in task.items:
            ent = item.entity.value
            props = [*item.bindings.values()]
            if ent == m.Builtins.Return:
                selects.extend([f"{sources[var]} as {self.namer.get(var)}" for var in props])
            elif ent == m.Builtins.RawData:
                mid = len(props)//2
                cols = props[:mid]
                vars = props[mid:]

                requires_union = False
                for col in cols:
                    has_var = any([isinstance(v, m.Var) and v.value is None for v in cast(list, col.value)])
                    if has_var:
                        requires_union = True
                        break
                if not requires_union:
                    rows = []
                    for i in range(len(cast(list, cols[0].value))):
                        row = [self.emit_var(cast(list, col.value)[i], sources) for col in cols]
                        rows.append(f"({','.join(row)})")
                    if len(froms):
                        froms.append(f", (VALUES {','.join(rows)}) AS RAW{item.id}")
                    else:
                        froms.append(f"(VALUES {','.join(rows)}) AS RAW{item.id}")
                else:
                    raws.append(item)

                for ix,var in enumerate(vars):
                    sources[var] = f"RAW{item.id}.column{ix+1}"
            elif item.action == m.ActionType.Bind:
                if isinstance(ent, m.Property):
                    prop_names = ["id", "value"]
                elif isinstance(ent, m.Task) or (isinstance(ent, m.Type) and ent.isa(m.Builtins.Relation)):
                    prop_names = [f"v{ix}" for ix in range(len(props))]
                elif isinstance(ent, m.Type):
                    prop_names = ["id"]
                else:
                    raise Exception("Bind on: " + str(ent))
                name = ent.name or f"T{ent.id}"
                pre.append(f"DROP VIEW IF EXISTS {name};")
                view = f"CREATE VIEW {name} AS"
                selects.extend([f"{sources.get(var, self.emit_var(var, sources))} AS {prop_names[ix]}" for ix, var in enumerate(props)])
                bind = item
            elif item.action == m.ActionType.Call:
                ent = cast(m.Type, ent)
                if ent.name in sql_filter:
                    wheres.append(f"{self.emit_var(props[0], sources)} {ent.name} {self.emit_var(props[1], sources)}")
                elif ent.name in sql_infix:
                    sources[props[-1]] = f"({self.emit_var(props[0], sources)} {ent.name} {self.emit_var(props[1], sources)})"
                elif ent == m.Builtins.make_identity:
                    args = cast(list, props[0].value)
                    vs = " || ".join([self.emit_var(prop, sources) for prop in args])
                    sources[props[-1]] = f"encode(sha1({vs}), 'base64')"
                elif ent.name == "range":
                    start, stop, step = [cast(int, prop.value) for prop in props]
                    froms.append(f"(VALUES {','.join([f'({i})' for i in range(start, stop, step)])}) AS range{item.id}")
                    sources[props[-1]] = f"range{item.id}.column1"
                elif isinstance(ent, m.Task) and len(ent.items):
                    print("SUB")
                else:
                    print("FUNC", item)
                    raise Exception("Support arbitrary SQL functions")
            elif isinstance(ent, m.Task) or (isinstance(ent, m.Type) and ent.isa(m.Builtins.Relation)):
                name = ent.name or f"T{ent.id}"
                joins = []
                for ix,prop in enumerate(props):
                    if sources.get(prop):
                        joins.append(f"{sources[prop]} = {name}.v{ix}")
                cur_from = name
                if len(joins):
                    cur_from = f"join {name} on {' and '.join(joins)}"
                froms.append(cur_from)
                for ix, prop in enumerate(props):
                    sources[prop] = f"{name}.v{ix}"
            elif isinstance(ent, m.Type):
                froms.append(ent.name)
                sources[props[0]] = f"{ent.name}.id"
            elif isinstance(ent, m.Property):
                source = sources[props[0]]
                sources[props[1]] = f"{ent.name}.value"
                froms.append(f"join {ent.name} on {ent.name}.id = {source}")

        for raw in raws:
            ent = raw.entity.value
            props = [*raw.bindings.values()]
            mid = len(props)//2
            cols = props[:mid]
            vars = props[mid:]
            unions = []
            for i in range(len(cols[0].value)):
                row = [self.emit_var(col.value[i], sources) + f" AS column{ix+1}" for ix, col in enumerate(cols)]
                sel = f"SELECT {','.join(row)}"
                if len(froms):
                    sel += f" FROM {','.join(froms)}"
                if len(wheres):
                    sel += f" WHERE {','.join(wheres)}"
                unions.append(sel)
            body = '\n     UNION\n    '.join(unions)
            froms.append(f", ({body}) AS RAW{raw.id}")

        query_parts = []
        if len(selects):
            query_parts.append("SELECT DISTINCT\n  " + ",\n  ".join(selects))
        if len(froms):
            query_parts.append("FROM\n  " + "\n  ".join(froms))
        if len(wheres):
            query_parts.append("WHERE\n  " + " AND\n  ".join(wheres))
        query = "\n".join(query_parts)

        if bind:
            self.existing_binds[bind.entity.value].append(query)
            query = "\n/*---------------------------------------*/\nUNION\n".join([textwrap.indent(binding, "  ") for binding in self.existing_binds[bind.entity.value]])

        if view:
            query = view + "\n" + textwrap.indent(query, "    ")

        query += ";"

        if len(pre):
            pre.append(query)
            return pre
        return query

#--------------------------------------------------
# Compiler
#--------------------------------------------------

class Compiler(c.Compiler):
    def __init__(self):
        passes = rel.Compiler().passes
        super().__init__(Emitter(), passes)

#--------------------------------------------------
# Executor
#--------------------------------------------------

class Executor():
    def __init__(self, database:str, engine:str|None, dry_run=False):
        self._engine = engine
        self._database = database
        self.compiler = Compiler()
        sqlite = cast(Any, sqlite3)
        sqlite.extensions.enable_all()
        self.conn = sqlite.connect(':memory:')

    def query(self, task:m.Task):
        start = time.perf_counter()
        statements = self.compiler.compile(task)
        time.perf_counter()
        for statement in statements[:-1]:
            self.conn.execute(statement)
        res = read_sql_query(statements[-1], self.conn)
        debugging.time("query", time.perf_counter() - start, res)
        return res

    def install(self, name, task:m.Task):
        start = time.perf_counter()
        statements = self.compiler.compile(task)
        time.perf_counter()
        for statement in statements:
            self.conn.execute(statement)
        debugging.time("install_batch", time.perf_counter() - start)

    def export_udf(self, name, inputs, out_fields, task):
        pass

def Graph(name, engine:str|None=None, dry_run=False):
    return dsl.Graph(Executor(name, engine, dry_run), name)
