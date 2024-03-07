# `relationalai.std.graphs.Edges.extend()`

```python
relationalai.std.graph.Edges.extend(prop: Property, **kwargs: Any) -> None
```

Add pairs of objects from a [`Property`](../../../Property.md) to a graph's edges.
Edge properties may be passed as keyword arguments to `**kwargs`.
You can use and display these properties in graph visualizations.
Objects produced by the `prop` producer are _not_ automatically added to the nodes of the graph
and must be explicitly added using [`Nodes.add()`](../Nodes/add.md) or [`Nodes.extend()`](../Nodes/extend.md).

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `prop` | [`Property`](../../../Property.md) | The property from which edges are to be added. |
| `**kwargs` | `Any` | Keyword arguments representing property name and value pairs. Values may be literals or `Producer` objects. |

## Returns

`None`.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with a `Person` type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.set(follows="Bob")

# Create a graph and extend the edges with the `Person.follows` property.
graph = Graph(model)
graph.nodes.extend(Person)
graph.edges.extend(Person.follows)
```

## See Also

[`Edges.add()`](./add.md) and [`Graph.edges`](../Graph/edges.md).
