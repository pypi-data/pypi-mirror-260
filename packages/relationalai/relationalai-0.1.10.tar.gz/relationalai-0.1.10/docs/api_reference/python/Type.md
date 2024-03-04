<!-- markdownlint-disable MD024 -->

# `Type`

Types are collections of objects.
You create types using the [`Model.Type()`](./Model.md#modeltype) method,
which returns an instance of the `Type` class.

```python
class relationalai.Type(model: Model, name: str)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model in which the type is created. |
| `name` | `str` | The name of the type. Type names must begin with a Unicode letter or an underscore followed by one or more Unicode letters, underscores, or numbers. |

## Example

Use [`Model.Type()`](./Model.md#modeltype) to create a `Type` object rather than constructing one directly:

```python
import relationalai as rai

# Create a new model.
model = rai.Model("myModel")

# Create a new type.
MyType = model.Type("MyType")
```

## Attributes and Methods

### `Type.add()`

```python
Type.add(self, *args, **kwargs) -> Instance
```

Adds a new object to the type and returns an [`Instance`](./Instance.md) representing that object.
Only call `Type.add()` from within a [rule](./Model.md#modelrule) or [query](./Model.md#modelquery) context.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | `Any` | Any additional types to which the object being added belongs. |
| `*kwargs` | `Any` | Properties that uniquely identify the object being added. |

#### Returns

An [`Instance`](./Instance.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("books")

# Create a type named Book.
Book = model.Type("Book")

# Add a book instance to the Book type.
with model.rule():
    Book.add(name="Foundation", author="Isaac Asimov")
```

You may add an object to multiple types simultaneously by passing the type objects as positional parameters:

```python
Fiction = model.type("Fiction")
SciFi = model.Type("SciFi")

with model.rule():
    Book.add(Fiction, SciFi, name="Foundation", author="Isaac Asimov")
```

This rule adds a new book object and classifies it as fiction and sci-fi.

Properties set with `.add()` are hashed internally to uniquely identify the object in the model.
These internal IDs are the values produced by `Instance` objects:

```python
with model.query() as select:
    book = Book()
    reponse = select(book)

print(response.results)
# Output:
#                      book
# 0  iikm1rGdR3jWQtS2XVUZDg
```

### `Type.__call__()`

```python
Type.__call__(self, *args, **kwargs) -> Instance
```

Returns an [`Instance`](./Instance.md) that produces objects from `Type`.
You must call a type from within a [rule](./Model.md#modelrule) or [query](./Model.md#modelquery) context.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | `Any` | Any additional types that found objects must have. |
| `*kwargs` | `Any` | Properties and values that found objects must have. |

#### Returns

An [`Instance`](./Instance.md) object.

#### Example

When you call a `Type` object without any arguments it returns an [`Instance`](./Instance.md)
that produces every object of that type:

```python
import relationalai as rai

model = rai.Model("books")

# Create Book, Fiction, and NonFiction types.
Book = model.Type("Book")
Fiction = model.Type("Fiction")
NonFiction = model.Type("NonFiction")

# Add some book instance to the Book type.
with model.rule():
    Book.add(Fiction, name="Foundation", author="Isaac Asimov")
    Book.add(NonFiction, name="Humble Pi", author="Matt Parker")

# Get the name of every book.
with model.query() as select:
    book = Book()
    response = select(book.name)

print(response.results)
# Output:
#          name
# 0  Foundation
# 1   Humble Pi
```

In English, this query says:
"Select `book.name` where `book` is a `Book` object."
In logic jargon, `book = Book()` binds the instance `book` to the `Book` collection.

Pass property values as keyword arguments when you call a type to
get an `Instance` that produces objects with those properties:

```python
# Who is the author of Foundation?
with model.query() as select:
    book = Book(name="Foundation")
    response = select(book.author)

print(response.results)
# Output:
#          author
# 0  Isaac Asimov
```

You may pass additional types as positional parameters to produce objects with multiple types:

```python
# What are the names of fiction books written by Isaac Asimov?
with model.query() as select:
    book = Book(Fiction, author="Isaac Asimov")
    response = select(book.name)

print(response.results)
# Output:
#          name
# 0  Foundation
```

If you pass a type only and no properties, the result is the intersection of objects in the types:

```python
with model.query() as select:
    book = Book(NonFiction)
    response = select(book.name, book.author)

print(response.results)
# Output:
#         name       author
# 0  Humble Pi  Matt Parker
```

### `Type.model`

Returns the `Model` to which the `Type` belongs.

#### Example

```python
import relationalai as rai

model = rai.Model("myModel")
MyType = model.Type("MyType")

print(model == MyType.model)
# Output:
# True
```

### `Type.name`

Returns the name of the type.

#### Example

```python
import relationalai as rai

model = rai.Model("myModel")
MyType = model.Type("MyType")

print(MyType.name)
# Output:
# 'MyType'
```

### `Type.__or__()`

```python
Type.__or__(self, __value: Any) -> TypeUnion
```

Types support the `|` operator for expressing the union of two types.

#### Returns

A `TypeUnion` object.
`TypeUnion` objects behave just like `Type` objects.

#### Example

```python
import relationalai as rai

model = rai.Model("books")

# Create Book, Fiction, NonFiction, Fantasy, and SciFi types.
Book = model.Type("Book")
Fiction = model.Type("Fiction")
NonFiction = model.Type("NonFiction")
Fantasy = model.Type("Fantasy")
SciFi = model.Type("SciFi")

# Add some book instance to the Book type.
with model.rule():
    Book.add(Fiction, Fantasy, name="The Hobbit", author="J.R.R. Tolkien")
    Book.add(Fiction, SciFi, name="Foundation", author="Isaac Asimov")
    Book.add(NonFiction, name="Humble Pi", author="Matt Parker")

# Get the names and authros of all books that are nonfiction or fantasy.
with model.query() as select:
    book = Book(NonFiction | Fantasy)
    response = select(book.name, book.author)

print(response.results)
# Output:
#          name          author
# 0   Humble Pi     Matt Parker
# 1  The Hobbit  J.R.R. Tolkien
```

In English, this query says:
"Select `book.name` and `book.author` where `book` is a `Book` object that is also a
`NonFiction` object or a `Fantasy` object."
