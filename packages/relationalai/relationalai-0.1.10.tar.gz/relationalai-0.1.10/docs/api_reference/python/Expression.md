# Expression

Expressions are [producers](./Producer.md) that produce the results of
a mathematical expression involving one or more [`Producer`](./Producer.md) objects.
You create expressions using operators like
[`+`](./Producer.md#producer__add__),
[`==`](./Producer.md#producer__eq__),
and [`>`](./Producer.md#producer__gt__)
with a [`Producer`](./Producer.md) object, all of which return an instance of the `Expression` class.

```python
class Expression(model: Model)
```

`Expression` is a subclass of [`Producer`](./Producer.md).

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model in which the expression is created. |

## Example

You create an `Expression` object when you use an operator like [`>`](./Producer.md#producer__gt__)
with a [`Producer`](./Producer.md) object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
   Person.add(name="Fred", age=39)
   Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values strictly greater than 36
    # and return an `Expression` object.
    person.age > 36
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0  Fred
```

The following operators can all be used with [`Producer`](./Producer.md) objects to create `Expression` objects:

- [`+`](./Producer.md#producer__add__)
- [`-`](./Producer.md#producer__sub__)
- [`*`](./Producer.md#producer__mul__)
- [`/`](./Producer.md#producer__truediv__)
- [`==`](./Producer.md#producer__eq__)
- [`!=`](./Producer.md#producer__ne__)
- [`>`](./Producer.md#producer__gt__)
- [`>=`](./Producer.md#producer__ge__)
- [`<`](./Producer.md#producer__lt__)
- [`<=`](./Producer.md#producer__le__)

## See Also

[`Producer`](./Producer.md)
