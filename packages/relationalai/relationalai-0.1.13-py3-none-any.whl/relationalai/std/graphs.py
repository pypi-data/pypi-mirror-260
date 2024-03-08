from collections import defaultdict
from copy import deepcopy
from typing import Any
from .. import dsl, errors
import gravis as gv
from . import rel

#--------------------------------------------------
# Errors
#--------------------------------------------------

def invalid_param(param:str, message:str):
    source = errors.Errors.call_source(4)
    marked = errors.mark_source(source, source.line, source.line) if source else ""
    content = f"""
    The [yellow]{param}[/yellow] parameter {message}

    {marked}
    """
    errors.print_source_error(source, "Invalid algorithm parameter", content)
    exit(1)

#--------------------------------------------------
# Validation
#--------------------------------------------------

def between(param:str, value, min, max):
    if value < min or value > max:
        invalid_param(param, f"must be between {min} and {max}")

def positive(param:str, value):
    if value <= 0:
        invalid_param(param, "must be positive")

#--------------------------------------------------
# Graph
#--------------------------------------------------

class Compute:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._lib = rel.rel.graph
        self._old_lib = getattr(rel, self._graph._lib_ref())

    def _config(self, **kwargs):
        return dsl.InlineRelation(self._graph.model, [
            *[(dsl.Symbol(k), v) for k, v in kwargs.items()],
        ])

    def pagerank(self, node, damping_factor=0.85, tolerance=1e-6, max_iter=20):
        between("damping_factor", damping_factor, 0, 1)
        positive("tolerance", tolerance)
        positive("max_iter", max_iter)

        config = self._config(
            graph=self._graph,
            damping_factor=damping_factor,
            tolerance=tolerance,
            max_iter=max_iter,
        )
        return self._lib.centrality.pagerank(config, node)

    #TODO: these are still in the old style graph lib
    def degree(self, node, weight=None):
        if not weight:
            return self._old_lib.degree(node)
        return self._old_lib.weighted_degree(node)

    def betweenness_centrality(self, node):
        return self._old_lib.betweenness_centrality(node)

    def degree_centrality(self, node):
        return self._old_lib.degree_centrality(node)

    def label_propagation(self, node):
        return self._old_lib.label_propagation(node)

    def weakly_connected_component(self, node):
        return self._old_lib.weakly_connected_component(node)
    
    def triangle_community(self, node):
        return self._old_lib.triangle_community(node)

    def infomap(self, node):
        config = self._config(graph=self._graph)
        return self._lib.community_detection.infomap(config, node)

class Nodes:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._type = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_nodes", 1)
        self._props = {}

    def _prop(self, name:str):
        if name not in self._props:
            self._props[name] = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_node_{name}", 2)
        return self._props[name]

    def extend(self, type:dsl.Type, **kwargs):
        with self._graph.model.rule():
            t = type()
            self.add(t, **kwargs)

    def add(self, node, **kwargs):
        self._type.add(node)
        for k, v in kwargs.items():
            if isinstance(v, dsl.Property):
                v = getattr(node, v._name)
            self._prop(k).add(node, v)

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["add", "extend"] or __name.startswith("_"):
            return super().__getattribute__(__name)
        return self._props[__name]

class Edges:
    def __init__(self, graph:'Graph'):
        self._graph = graph
        self._type = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_edges", 2)
        self._props = {}

    def _prop(self, name:str):
        if name not in self._props:
            self._props[name] = dsl.RawRelation(self._graph.model, f"graph{self._graph.id}_edge_{name}", 3)
        return self._props[name]

    def extend(self, prop:'dsl.Property|Edge', **kwargs):
        type = prop._provider
        with self._graph.model.rule():
            t = type()
            self.add(t, getattr(t, prop._name), **kwargs)

    def add(self, from_:Any, to:Any, **kwargs):
        self._type.add(from_, to)
        for k, v in kwargs.items():
            self._prop(k).add(from_, to, v)

    def __getattribute__(self, __name: str) -> Any:
        if __name in ["add", "extend"] or __name.startswith("_"):
            return super().__getattribute__(__name)
        return self._props[__name]

class Graph:
    def __init__(self, model:dsl.Graph, undirected=False):
        self.model = model
        self.id = dsl.next_id()
        self.compute = Compute(self)
        self.nodes = Nodes(self)
        self.edges = Edges(self)
        self.undirected = undirected
        self._last_fetch = None

        graph_type = "undirected_graph" if undirected else "directed_graph"
        self.model.install_raw(f"""
        bound {self.nodes._type._name}
        bound {self.edges._type._name}
        def {self._graph_ref()} = {graph_type}[{self.edges._type._name}]
        @inline
        def {self._lib_ref()} = rel:graphlib[{self._graph_ref()}]
        """)

        # Add a rule that makes all nodes used in edges are also added to
        # the nodes relation
        with model.rule():
            a, b = dsl.Vars(2)
            self.edges._type(a, b)
            self.nodes._type.add(a)
            self.nodes._type.add(b)

    def _graph_ref(self):
        return f"graph{self.id}"

    def _lib_ref(self):
        return f"graphlib{self.id}"

    def _to_var(self):
        return getattr(rel, self._graph_ref())._to_var()

    #--------------------------------------------------
    # Fetch
    #--------------------------------------------------

    def fetch(self):
        code = []
        code.append(f"def output:nodes(n) = {self.nodes._type._name}(n)")
        for name, prop in self.nodes._props.items():
            code.append(f"def output:nodes:{name}(n, v) = {prop._name}(n, v)")
        code.append(f"def output:edges(a,b) = {self.edges._type._name}(a,b)")
        for name, prop in self.edges._props.items():
            code.append(f"def output:edges:{name}(a,b,v) = {prop._name}(a,b,v)")

        output = {"nodes": defaultdict(dict), "edges": defaultdict(dict)}
        results = self.model.exec_raw("\n".join(code), raw_results=True)
        for set in results.results:
            path = [v[1:] for v in set["relationId"].split("/")[2:] if v[0] == ":"]
            if path[0] not in ["nodes", "edges"]:
                continue
            cur = output[path[0]]
            if path[0] == "nodes":
                if len(path) == 1:
                    for (n,) in set["table"].itertuples(index=False):
                        cur[n]
                else:
                    for (n,v) in set["table"].itertuples(index=False):
                        cur[n][path[1]] = v
            elif path[0] == "edges":
                if len(path) == 1:
                    for (a,b) in set["table"].itertuples(index=False):
                        cur[(a,b)]
                else:
                    for (a,b,v) in set["table"].itertuples(index=False):
                        cur[(a,b)][path[1]] = v
            else:
                raise Exception(f"Unexpected path: {path}")
        self._last_fetch = output
        return output

    #--------------------------------------------------
    # Visualize
    #--------------------------------------------------

    default_visual_props = {
        "node": {
            "color": "black",
            "opacity": 1,
            "size": 10,
            "shape": "circle",
            "border_color": "black",
            "border_size": 1,
            "label_color": "black",
            "label_size": 10,
        },
        "edge": {
            "color": "#999",
            "opacity": 1,
            "size": 2,
            "shape": "circle",
            "border_color": "#999",
            "border_size": 1,
            "label_color": "black",
            "label_size": 10,
            "arrow_size": 4,
            "arrow_color": "#999",
        }
    }

    _style_map = {
        "arrow_size": "arrow_size",
        "arrow_color": "arrow_color",
    }


    def _visual_props(self, prop_def, metadata):
        for k, v in prop_def.items():
            if callable(v):
                metadata[k] = v(metadata)
        return metadata

    def visualize(self, three=False, style={"node": {}, "edge": {}}, **kwargs):
        data = self._last_fetch
        if not data:
            data = self.fetch()

        style = deepcopy(style)
        if "node" not in style:
            style["node"] = {}
        if "edge" not in style:
            style["edge"] = {}
        merged_style = deepcopy(self.default_visual_props)
        for category in ["node", "edge"]:
            for k, v in style.get(category, {}).items():
                if not callable(v):
                    merged_style[category][k] = v
        flat_style = {self._style_map.get(k, f"{type}_{k}"): v
                        for type, category in merged_style.items()
                        for k, v in category.items()}

        graph1 = {
            "graph": {
                "directed": not self.undirected,
                "metadata": flat_style,
                "nodes": {
                    node_id: {
                        **({"label": info["label"]} if "label" in info else {}),
                        "metadata": self._visual_props(style["node"], info),
                    }
                    for (node_id, info) in data["nodes"].items()
                },
                "edges": [
                    {"source": source, "target": target, "metadata": self._visual_props(style["edge"], info)}
                    for ((source, target), info) in data["edges"].items()
                ],
            }
        }

        vis = gv.vis if not three else gv.three
        fig = vis(graph1, edge_label_data_source='label', node_label_data_source='label', edge_curvature=0.4, **kwargs)
        return fig


#--------------------------------------------------
# Edge
#--------------------------------------------------

class Edge:
    def __init__(self, type:Any, from_:Any, to:Any):
        # raise NotImplementedError()
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __getattribute__(self, __name: str) -> Any:
        pass

    def __getitem__(self, item):
        return self

#--------------------------------------------------
# Path
#--------------------------------------------------

class Path:
    def __init__(self, *args):
        self.edges = []
        self.nodes = []
        pass

    def __getitem__(self, item):
        return self

#--------------------------------------------------
# Exports
#--------------------------------------------------

__all__ = ["Graph", "Edge", "Path"]