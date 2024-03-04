<!-- markdownlint-disable MD024 -->

# `Context`

Contexts execute blocks of code written in RelationalAI's declarative query builder syntax.
You create contexts using [`Model`](./Model.md) methods,
such as [`Model.query()`](./Model.md#modelquery) and [`Model.rule()`](./Model.md#modelrule),
that return an instance of the `Context` class.

```python
class relationalai.Context(model: Model, dynamic: bool = False)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model for which the context is created. |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic contexts support Python control flow as query builder macros. |

## Example

You create contexts using [`Model`](./Model.md) methods rather than creating a `Context` instance directly.
The primary contexts are [`Model.rule()`](./Model.md#modelrule) and [`Model.query()`](./Model.md#modelquery).

`Context` objects are [context managers](https://docs.python.org/3/glossary.html#term-context-manager).
You use them in [`with` statements](https://docs.python.org/3/reference/compound_stmts.html#with):

```python
import relationalai as rai

model = rai.Model("myModel")
MyType = model.Type("MyType")

# Create a rule context with `model.rule()` that adds an object to `MyType`.
with model.rule():
    MyType.add(name="my first object")

# Create a query context with `model.query()` to query the model.
with model.query() as select:
    obj = MyType()
    response = select(obj.name)

print(response.results)
# Output:
#               name
# 0  my first object
```

The following `Model` methods all return `Context` objects:

- [`Model.found()`](./Model.md/#modelfound)
- [`Model.not_found()`](./Model.md#modelnot_found)
- [`Model.ordered_choice()`](./Model.md#modelordered_choice)
- [`Model.query()`](./Model.md#modelquery)
- [`Model.rule()`](./Model.md#modelrule)
- [`Model.scope()`](./Model.md#modelscope)
- [`Module.union()`](./Model.md#modelunion)

## Attributes and Methods

### `Context.__enter__()`

```python
Context.__enter__() -> ContextSelect
```

`Context` objects are [context managers](https://docs.python.org/3/glossary.html#term-context-manager).
Although you can call the `.__enter__()` method directly, it is typically called by a
[`with` statement](https://docs.python.org/3/reference/compound_stmts.html#with).

In a `with` statement, Python calls the context manager's `.__enter__()` method before executing the `with` block.
Optionally, you may give the [`ContextSelect`](./ContextSelect.md) object returned by `.__enter__()` a name
in the `as` part of the `with` statement.
After the `with` block executes,
the `with` statement automatically executes the [`Context.__exit__()`](#context__exit__) method.

#### Returns

A [`ContextSelect`](./ContextSelect.md) object.

#### Example

You create rule contexts with [`Model.rule()`](./Model.md#modelrule)
and query contexts with [`Model.query()`](./Model.md#modelquery).
The `Model.query()` context's `.__enter__()` method returns a [`ContextSelect`](./ContextSelect.md) object,
typically given the name `select`, that you use to select query results:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

# The `with` statement calls the `model.rule()` context's
# `.__enter__()` method automatically. The `ContextSelect` object
# returned by `.__enter__()` is not typically used in a rule.
with model.rule():
    Person.add(name="Fred")

# The `with` statement calls the `model.query()` context's
# `.__enter__()` method and assigns the `ContextSelect`
# object it returns to a Python variable named `select`.
with model.query() as select:
    person = Person()
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0  Fred
```

[Calling `select`](./ContextSelect.md#contextselect__call__) returns the same `Context` object created by
[`model.query()`](./Model.md#modelquery) in the `with` statement.
The results of the query are stored as a pandas DataFrame
and are accessible via the [`Context.results`](#contextresults) attribute.

#### See Also

[`Context.__exit__()`](#context__exit__) and [`ContextSelect`](./ContextSelect.md).

### `Context.__exit__()`

```python
Context.__exit__(*args) -> None
```

`Context` objects are [context managers](https://docs.python.org/3/glossary.html#term-context-manager).
Although you can call the `.__exit__()` method directly, it is typically called by a
[`with` statement](https://docs.python.org/3/reference/compound_stmts.html#with).

In a `with` statement, Python calls the context manager's [`.__enter__()`](#context__enter__) method
before executing the `with` block.
After the `with` block executes, the `with` statement automatically executes the `.__exit__()` method.
`.__exit__()` translates query builder code inside the `with` block into a RelationalAI query.

#### Returns

`None`

#### Example

The `.__exit__()` method is called automatically in a `with` statement:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

# The `with` statement calls the `model.rule()` context's `.__exit__()`
# method automatically after the `with` block terminates.
# `.__exit__()` translates the query builder code into a RelationalAI query.
with model.rule():
    Person.add(name="Fred")

# The `with` statement calls the `model.query()` context's `.__exit__()`
# method automatically after the `with` block terminates.
# `.__exit__()` translates the query builder code into a RelationalAI query,
# sends the query to RelationalAI, and blocks until the results are returned.
with model.query() as select:
    person = Person()
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0  Fred
```

#### See Also

[`Context.__enter__()`](#context__enter__)

### `Context.__iter__()`

```python
Context.__iter__() --> Iterator
```

Returns an iterator over rows of [`Context.results`](#contextresults) that is equivalent to:

```python
Context.results.itertuples(index=False)`
```

See [`DataFrame.itertuples()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.itertuples.html)
for more information.

#### Returns

A Python [iterator](https://docs.python.org/3/glossary.html#term-iterator).

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Bonnie")
    Person.add(name="Clyde")

with model.query() as select:
    person = Person()
    response = select(person.name)

for i, row in enumerate(response, start=1):
    print(f"Person {i} is named {row.name}.")
# Output:
# Person 1 is named Bonnie.
# Person 2 is named Clyde.
```

#### See Also

[`Context.results`](#contextresults)

### `Context.model`

Returns the [`Model`](./Model.md) object for which the context was created.

#### Returns

A [`Model`](./Model.md) object.

#### Example

```python
import relationalai as rai

model = rai.model("people")
Person = model.Type("Person")

with model.query() as select:
    person = Person()
    response = select(person.name)

# `response` is the `Context` object created by `model.query()`.
print(response.model == model)
# Output:
# True
```

Calling a [`ContextSelect`](./ContextSelect.md) object, like `select` in the preceding query, returns its `Context` object.
In this case, `response` is the `Context` object created by [`model.query()`](./Model.md#modelquery) in the `with` statement.

#### See Also

[`Model`](./Model.md)

### `Context.results`

Returns a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
containing results selected in a [`model.query()`](./Model.md#modelquery) context.

#### Returns

A pandas [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) object.

#### Example

Access `.results` after selecting results in a query:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Alice", age="31")
    Person.add(name="Alice", age="27")
    Person.add(name="Bob", author="19")

with model.query() as select:
    person = Person()
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name age
# 0  Alice  27
# 1  Alice  31
# 2    Bob  19
```

Calling a [`ContextSelect`](./ContextSelect.md) object, like `select` in the preceding query, returns its `Context` object.
In this case, `response` is the `Context` object created by [`model.query()`](./Model.md#modelquery) in the `with` statement.

By default, results are in ascending [lexicographic order](https://en.wikipedia.org/wiki/Lexicographic_order).
In the preceding example, all names beginning with `A` come first, followed by names starting with `B`, and so on.
If two names are the same, such as the two people named `"Alice"`,
the remaining columns are used to determine the sort position of the rows.
In this case, the row for the 27-year-old Alice comes first.

See the [pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)
for details about everything you can do with a DataFrame.

#### See Also

[`ContextSelect`](./ContextSelect.md) and [`Model.query()`](./Model.md#modelquery).
