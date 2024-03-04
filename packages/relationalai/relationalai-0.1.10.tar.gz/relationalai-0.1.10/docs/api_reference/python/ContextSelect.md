<!-- markdownlint-disable MD024 -->

# ContextSelect

`ContextSelect` objects are returned by the [`Context.__enter__()`](./Context.md#context__enter__) method.
They are primarily used to select results in [query](./Model.md#modelquery) contexts.
`ContextSelect` objects are also used in [`Model.ordered_choice()`](./Model.md#modelordered_choice)
and [`Model.union()`](./Model.md#modelunion) contexts.

```python
class relationalai.ContextSelect(context: Context)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `context` | [`Context`](./Context.md) | The `Context` object for which the `ContextSelect` object is created. |

## Example

The [`Context.__enter__()`](./Context.md#context__enter__) method returns a `ContextSelect` object when called
in a [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#with).
An example is the `select` object used in [query](./Model.md#modelquery) contexts:

```python
import relationalai as rai

model = rai.Model("books")
Book = model.Type("Book")

# Add a book to the model.
with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov")
    Book.add(title="Humble Pi", author="Matt Parker")

# Get all books in the model.
# `select` is a `ContextSelect` object returned by `model.query().__enter__()`.
with model.query() as select:
    book = Book()
    response = select(book.name, book.author)

print(response.results)
# Output:
#         title        author
# 0  Foundation  Isaac Asimov
# 1   Humble Pi   Matt Parker
```

`ContextSelect` objects are callable.
The preceding example calls the `select` object to select results in the query.
You may only call `ContextSelect` objects in a [query](./Model.md#modelquery) context.

Other contexts, like [`Model.ordered_choice()`](./Model.md#modelordered_choice)
and [`Model.union()`](./Model.md#modelunion), also use a `ContextSelect` object.
In these contexts, the `ContextSelect` object works as a collection of objects:

```python
with model.query() as select:
    book = Book()
    # `union` is a `ContextSelect` object created by the
    # `model.union().__enter__()` method. The `union.add()`
    # method is used to "select" objects based on conditions and
    # add them to the `union` collection.
    with model.union() as union:
        with book.author == "Isaac Asimov":
            union.add(book)
        with book.title == "Humble Pi":
            union.add(book)
    response = select(union.title, union.author)

print(response.results)
# Output:
#         title        author
# 0  Foundation  Isaac Asimov
# 1   Humble Pi   Matt Parker
```

Properties of objects added to a `ContextSelect` object via [`ContextSelect.add()`](#contextselectadd)
may be accessed directly thanks to [`ContextSelect.__getattribute__()`](#contextselect__getattribute__).
For instance, in the preceding example, the `.title` and `.author` properties of
`Book` objects in `union` are accessed as `union.title` and `union.author`.

## Attributes and Methods

### `ContextSelect.add()`

```python
ContextSelect.add(item: Any, **kwargs: Any) -> None
```

Adds an item to a `ContextSelect` object.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `item` | `Any` | The item to be added to the collection. |
| `kwargs` | `Any` | Optional keyword arguments that set context-specific properties on items in the collection. |

#### Returns

`None`

#### Example

```python
import relationalai as rai

model = rai.Model("books")
Book = model.Type("Book")

# Add some books to the model.
with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov", year=1951)
    Book.add(title="Humble Pi", author="Matt Parker", year=2019)

# Get all books authored by Isaac Asimov or published after 1950.
with model.query() as select:
    book = Book()
    with model.union() as union:
        with book.author == "Isaac Asimov":
            union.add(book, message="authored by Asimov")
        with book.year > 1950:
            union.add(book, message="published after 1950")
    response = select(union.title, union.author, union.message)

print(response.results)
# Output:
#         title        author                     v
# 0  Foundation  Isaac Asimov    authored by Asimov
# 1  Foundation  Isaac Asimov  published after 1950
# 2   Humble Pi   Matt Parker  published after 1950
```

Here, `union` is a `ContextSelect` object returned by the
[`model.union().__enter__()`](./Context.md#context__enter__) method.

Only `with` statements may appear in a `Model.union()` context.
Each `with` statement describes a condition that necessitates inclusion in the union
and calls `union.add()` to add an object to the union.
The preceding example adds books authored by Isaac Asimov and books published after 1950 to `union`.

The `message` keyword argument adds a `message` property to objects in `union`.
Multiple `message` values are set on objects for which multiple conditions apply.
Properties added to items in a `ContextSelect` are properties of the `ContextSelect` object, _not_ the item.
The `union` object has the `message` property in the preceding example, not `Book` objects.

Calling `.add()` on the same `ContextSelect` object with different keyword arguments raises an exception.
Since `.add()` sets a `message` property the first time it's called in the preceding example,
so must the second call to `.add()`.

Note that the column for the `.message` property in the results has the generic name `v`.
You may change the column name using [`model.alias()`](./Model.md#modelalias):

```python
with model.query() as select:
    book = Book()
    with model.union() as union:
        with book.author == "Isaac Asimov":
            union.add(book, message="authored by Asimov")
        with book.year > 1950:
            union.add(book, message="published after 1950")
    response = select(
        union.title, union.author, model.alias(union.message, "message")
    )

print(response.results)
# Output:
#         title        author               message
# 0  Foundation  Isaac Asimov    authored by Asimov
# 1  Foundation  Isaac Asimov  published after 1950
# 2   Humble Pi   Matt Parker  published after 1950
```

#### See Also

[`ContextSelect.__getattribute__()`](./ContextSelect.md#contextselect__getattribute__),
[`Model.ordered_choice()`](./Model.md#modelordered_choice),
and [`Model.union()`](./Model.md#modelunion)

### `ContextSelect.__call__()`

```python
ContextSelect.__call__(*args: Producer) -> Context
```

Selects the data to be returned by a query and returns the `ContextSelect` object's [`Context`](./Context.md) object.
You may only call `ContextSelect` objects within a [query](./Model.md#modelquery) context.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `args` | `Producer` | The data to be returned in query results. |

#### Returns

A [`Context`](./Context.md) object.

#### Example

In a [`Model.query()`](./Model.md#modelquery) context, the `ContextSelect` object returned by
[`Model.query().__enter__()`](./Context.md#context__enter__) is called inside the `with` block
to select query results:

```python
import relationalai as rai

model = rai.Model("books")
Book = model.Type("Book")

# Add a book to the model.
with model.rule():
    Book.add(name="Foundation", author="Isaac Asimov")

# Get the names of all of the books in the model.
# `select` is a `ContextSelect` object and it is called to return the
# `book.name` property for each book found by the query.
with model.query() as select:
    book = Book()
    response = select(book.name)

print(response.results)
# Output:
#         title        author
# 0  Foundation  Isaac Asimov
```

#### See Also

[`Context.__enter__()`](./Context.md#context__enter__) and [`Model.query()`](./Model.md#modelquery).

### `ContextSelect.__getattribute__()`

```python
ContextSelect.__get_attribute__(name: str) -> Instance
```

Gets an [`InstanceProperty`](./InstanceProperty.md) representing the property called `name` of
objects contained in the `ContextSelect` object.
Properties may be those created with [`Type.add()`](./Type.md#typeadd)
or [`ContextSelect.add()`](./ContextSelect.md#contextselectadd).

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `name` | `str` | The name of the property to get. |

#### Returns

An [`Instance`](./Instance.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("books")
Book = model.Type("Book")

# Add some books to the model.
with model.rule():
    Book.add(title="Foundation", author="Isaac Asimov", year=1951)
    Book.add(title="Humble Pi", author="Matt Parker", year=2019)

# Get all books authored by Isaac Asimov or published after 1950.
with model.query() as select:
    book = Book()
    with model.union() as union:
        with book.author == "Isaac Asimov":
            union.add(book, message="authored by Asimov")
        with book.year > 1950:
            union.add(book, message="published after 1950")
    # Select the `.title`, `.author`, and `.message` properties of
    # objects in `union`. Note that `.title` and `.author` were created
    # by `Book.add()`, whereas `.message` was created by `union.add()`.
    response = select(union.title, union.author, union.message)

print(response.results)
# Output:
#         title        author                     v
# 0  Foundation  Isaac Asimov    authored by Asimov
# 1  Foundation  Isaac Asimov  published after 1950
# 2   Humble Pi   Matt Parker  published after 1950
```

#### See Also

[`Model.ordered_choice()`](./Model.md#modelordered_choice) and [`Model.union()`](./Model.md#modelunion).
