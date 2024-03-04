<!-- markdownlint-disable MD024 -->

# InstanceProperty

Instance properties are [producers](./Producer.md) that produce property values of objects in a [model](./Model.md).
You create properties using the [`Type.add()`](./Type.md#typeadd) and [`Instance.set()`](./Instance.md#instanceset) methods,
which return [`Instance`](./Instance.md) objects.
You access properties as [`Instance` attributes](./Producer.md#producer__getattribute__),
which return instances of the `InstanceProperty` class.

```python
class InstanceProperty(model: Model)
```

The `InstanceProperty` class is a subclass of [`Producer`](./Producer.md).

## Parameters

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model in which the instance property is created. |

## Example

You do not create `InstanceProperty` objects directly.
Accessing a property as an [`Instance`](./Instance.md) attribute returns an `InstanceProperty` object:

```python
import relationalai as rai

model = rai.Model("books")
Book = model.Type("Book")

with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov")

with model.query() as select:
    book = Book()
    # Both `book.author` and `book.name` are `InstanceProperty` objects.
    book.author == "Isaac Asimov"
    response = select(book.name)
```

`InstanceProperty` objects are `Producer` objects and support the same attributes and methods.
See [`Producer`](./Producer.md) for details.

## See Also

[`Producer`](./Producer.md) and [`Instance`](./Instance.md).
