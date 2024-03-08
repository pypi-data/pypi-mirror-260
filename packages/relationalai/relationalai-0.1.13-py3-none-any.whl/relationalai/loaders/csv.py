
import numpy
import pandas
from ..dsl import build, RelationRef, Graph
from ..std import rel
from ..metamodel import ActionType, Builtins, Var
from datetime import date, datetime

def df_type(df_type_name):
    match df_type_name:
        case "bool":
            type = Builtins.Bool
        case "int64":
            type = Builtins.Number
        case "float64":
            type = Builtins.Number
        case _:
            type = Builtins.String
    return type

def safe_name(file:str) -> str:
    return file.replace("/", "_").replace(".", "_")

class ExternalRow:
    def __init__(self, data, columns):
        self._data = data
        self._columns = columns

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)
        return self._data[index]

    def __getattribute__(self, name):
        if name in ["_data", "_columns"]:
            return object.__getattribute__(self, name)
        if name in self._columns:
            return self._data[self._columns.index(name)]
        return object.__getattribute__(self, name)

# See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# for keyword arg docs.
def load_file(graph:Graph, csv_file, **kwargs):
    df = pandas.read_csv(csv_file, **kwargs)

    # create subqueries for each column that consist of a data object
    # and a bind for the column relation, also create a data ref
    # add a range for the id
    # when a dataref is used, it should add a get for the column relation
    # the rest just works?

    id = rel.range(0, len(df), 1)
    items = []
    for col in df.columns:
        sub = df[[col]]
        col_type = df_type(df[col].dtype)
        with graph.scope(dynamic=True):
            # By setting Builtins.RawData on the task, we're telling the denester to not
            # put a reference to the parent scope in this one
            graph._stack.active()._task.parents.append(Builtins.RawData)
            v1 = []
            v2 = []
            for (i, v) in sub.itertuples():
                if v is not None and v != "" and v is not False and (isinstance(v,str) or isinstance(v, date) or isinstance(v, datetime) or not numpy.isnan(v)):
                    v1.append(i)
                    v2.append(v)

            v1_var = Var(type=Builtins.Number)
            v2_var = Var(name=col, type=col_type)
            graph._action(
                build.relation_action(ActionType.Get, Builtins.RawData, [Var(value=v1), Var(value=v2), v1_var, v2_var])
            )
            temp = build.relation(safe_name(csv_file) + "_" + col, 2)
            graph._action(
                build.relation_action(ActionType.Bind, temp, [v1_var, v2_var])
            )
            usage_var = Var(name=col, type=col_type)
            items.append(RelationRef(graph, temp, [id, usage_var]))

    return ExternalRow(items, [c for c in df.columns])
