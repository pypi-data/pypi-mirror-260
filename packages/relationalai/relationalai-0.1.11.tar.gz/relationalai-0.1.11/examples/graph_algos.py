# pyright: reportUnusedExpression=false
import relationalai as rai
from relationalai.std.graphs import Graph
from relationalai.std.aggregates import sum
import rich

#--------------------------------------------------
# Types
#--------------------------------------------------

model = rai.Model("MyCoolDatabase")
Person = model.Type("Person")
Criminal = model.Type("Criminal")
Transaction = model.Type("Transaction")

#--------------------------------------------------
# Load data
#--------------------------------------------------

with model.rule():
    joe = Person.add(name="Joe")
    jane = Person.add(name="Jane")
    bob = Person.add(name="Bob")
    dylan = Person.add(Criminal, name="Dylan")

    joe.set(knows=jane)
    jane.set(knows=bob)
    bob.set(knows=joe)
    bob.set(knows=dylan)
    dylan.set(knows=joe)

    Transaction.add(from_=joe, to=jane, amount=100)
    Transaction.add(from_=joe, to=jane, amount=1000)
    Transaction.add(from_=joe, to=jane, amount=10)
    Transaction.add(from_=joe, to=bob, amount=10)

#--------------------------------------------------
# Graph
#--------------------------------------------------

graph = Graph(model)
nodes, edges = graph.nodes, graph.edges

nodes.extend(Person, label=Person.name)
nodes.extend(Criminal, criminal=True)
edges.extend(Person.knows, label="knows")

with model.rule():
    t = Transaction()
    weight = sum(t, t.amount, per=[t.from_, t.to])
    edges.add(t.from_, t.to, label="Transfer", weight=weight)

with model.rule():
    p = Person()
    rank = graph.compute.pagerank(p)
    nodes.add(p, rank=rank * 5)

#--------------------------------------------------
# Paths
#--------------------------------------------------

# Transfer = Edge(Transaction, Transaction.from_, Transaction.to)
# Teller = Edge(Transaction, Transaction.from_, Transaction.teller)

# with model.query() as select:
#     p = Path(Person, Transfer, Criminal)
#     select(p)

# with model.query() as select:
#     person = Person(name="John")
#     t = Transfer(); t.amount > 10000
#     p = Path(person, t, Criminal)
#     select(p)

# with model.query() as select:
#     p = Path(Person, Transfer[0:2], Criminal)
#     select(p)

# with model.query() as select:
#     p = Path(Person, Transfer, Person, Knows, Criminal)[1:2]
#     select(p)

# with model.query() as select:
#     t = Transfer(); t.amount > 10000
#     sub = Path(Person, t, Person)
#     p = Path(Person, sub[1:3], Criminal)
#     select(p[0])

#--------------------------------------------------
# Notes
#--------------------------------------------------
"""

Extends is a convenient way to take an existing set and add it to the graph, but
arbitrary logic can be used with nodes.add and edges.add to have explicit control:

    with model.rule():
        p = Person()
        nodes.add(p, label=p.name)
        with Criminal(p):
            nodes.add(p, color="red")
        edges.add(p, p.knows, color="#aaa")

If we were in SPCS, the data would come from snowflake tables which likely represent
hyperedges and so we might have N logical edges coming from a single table:

    Transfer = Edge(Transaction, Transaction.from_, Transaction.to)
    Teller = Edge(Transaction, Transaction.from_, Transaction.teller)

    edges.extend(Transfer)
    edges.extend(Teller)
"""

#--------------------------------------------------
# Go
#--------------------------------------------------

data = graph.fetch()
rich.print(data)
graph.visualize(three=True, style={
    "node": {
        "color": lambda x: "red" if x.get("criminal") else "blue",
        "size": lambda x: (x["rank"] * 2) ** 2
    },
    "edge": {
        "color": "yellow",
    }
}).display()