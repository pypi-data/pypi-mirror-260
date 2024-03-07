import gravis as gv
import relationalai as rai

model = rai.Model("MyCoolDatabase")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe")
    jane = Person.add(name="Jane")
    bob = Person.add(name="Bob")

    joe.set(knows=jane)
    jane.set(knows=bob)
    bob.set(knows=joe)

with model.query() as select:
    p = Person()
    edges = select(p, p.knows)

with model.query() as select:
    p = Person()
    nodes = select(p, p.name)

print(nodes.results)
print(edges.results)

graph1 = {
    'graph': {
        'directed': True,
        'metadata': {
            'arrow_size': 5,
            'background_color': 'black',
            'edge_size': 3,
            'edge_label_size': 0,
            'edge_label_color': 'white',
            'edge_color': '#777',
            'node_size': 15,
            'node_color': 'white',
            'node_label_color': 'white',
            'node_label_size': 10,
        },
        'nodes': {
            node_id: {'metadata': {'name': name}} for (node_id, name) in nodes
        },
        'edges': [
            {'source': source, 'target': target} for (source, target) in edges
        ],
    }
}

fig = gv.vis(graph1, show_edge_label=True, node_label_data_source='name')
fig.display()