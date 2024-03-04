<!-- markdownlint-disable MD024 -->

# Producer

`Producer` objects represent an unknown value in a context.
When a [query](./Model.md#modelquery) context is evaluated,
the values matching the context's constraints are produced.
The `Producer` class is the base class for different types of producers,
such as [`Instance`](./Instance.md) objects, which produce the IDs of objects in your model,
or [`InstanceProperty`](./InstanceProperty.md) objects, which produce object property values.

```python
class Producer(model: Model)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model in which the producer is created. |

## Example

`Producer` objects show up all over the place:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    # `Type.add()` returns an `Instance` object, which is a `Producer`.
    fred = Person.add(name="Fred", age=39)
    fred.set(favorite_color="green")

with model.query() as select:
    # Calling a Type returns an `Instance`.
    person = Person()

    # Accessing a property returns an `InstanceProperty` object,
    # which is a `Producer`.
    name = person.name
    age = person.age

    # Operators return an `Expression` object, which is a `Producer`.
    age > 30

    response = select(name, age)

print(response.results)
# Output:
#    name  age
# 0  Fred   39
```

The following classes are all subclasses of `Producer`:

- [`Instance`](./Instance.md)
- [`InstanceProperty`](./InstanceProperty.md)
- [`Expression`](./Expression.md)

## Attributes and Methods

### `Producer.__add__()`

```python
Producer.__add__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the sum of the `Producer` values and `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

You may sum a `Producer` with a number literal:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    age_after_next_birthday = person.age + 1
    response = select(person.name, age_after_next_birthday)

print(response.results)
# Output:
#     v
#     name   v
# 0   Fred  40
# 1  Wilma  37
```

You may also sum two `Producer` objects:

```python
with model.rule():
    fred = Person(name="Fred")
    fred.set(cash=100.0, savings=200.0)

with model.rule():
    wilma = Person(name="Wilma")
    wilma.set(cash=90.0, savings=310.0)

with model.query() as select:
    person = Person()
    # `person.cash` and `person.savings` return `InstanceProperty`
    # objects, which are also `Producer` objects.
    total_assets = person.cash + person.savings
    response = select(person.name, total_assets)

print(response.results)
# Output:
#     name      v
# 0   Fred  300.0
# 1  Wilma  400.0
```

#### See Also

[`Producer.__mul__()`](#producer__mul__),
[`Producer.__sub__()`](#producer__sub__),
and [`Producer.__truediv__()`](#producer__truediv__).

### `Producer.__radd__()`

```python
Producer.__radd__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the sum of the `Producer` values and `other`.
`.__radd__()` is implemented so that you may use a non-`Producer` object as the left operand.

#### See Also

[`Producer.__add__()`](#producer__add__)

### `Producer.__mul__()`

```python
Producer.__mul__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) the produces the product of the `Producer` values and `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

You may multiply a `Producer` object by a number literal:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    double_age = person.age * 2
    response = select(person.name, double_age)

print(response.results)
# Output:
#     name   v
# 0   Fred  78
# 1  Wilma  72
```

You may also multiply two `Producer` objects:

```python
with model.rule():
    fred = Person(name="Fred")
    fred.set(hours=30.0, wage=20.0)

with model.rule():
    wilma = Person(name="Wilma")
    wilma.set(hours=40.0, wage=30.0)

with model.query() as select:
    person = Person()
    # `person.hours` and `person.wage` return `InstanceProperty`
    # objects, which are also `Producer` objects.
    pay = person.hours * person.wage
    response = select(person.name, pay)

print(response.results)
# Output:
#     name       v
# 0   Fred   600.0
# 1  Wilma  1200.0
```

#### See Also

[`Producer.__add__()`](#producer__add__),
[`Producer.__sub__()`](#producer__sub__),
and [`Producer.__truediv__()`](#producer__truediv__).

### `Producer.__rmul__()`

```python
Producer.__rmul__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the product of `Producer` values and `other`.
`.__rmul__()` is implemented so that you may use a non-`Producer` object as the left operand.

#### See Also

[`Producer.__mul__()`](#producer__mul__)

### `Producer.__sub__()`

```python
Producer.__sub__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the difference between the `Producer` values and `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

You may subtract a number literal from a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # `person.age` returns an `InstanceProperty` object,
    # which are also `Producer` objects.
    years_as_adult = person.age - 18
    response = select(person.name, years_as_adult)

print(response.results)
# Output:
#     name   v
# 0   Fred  21
# 1  Wilma  18
```

You may also subtract two `Producer` objects:

```python
with model.rule():
    fred = Person(name="Fred")
    fred.set(expected_retirement_age=65)

with model.rule():
    wilma = Person(name="Wilma")
    wilma.set(expected_retirement_age=62)

with model.query() as select:
    person = Person()
    # `person.age`, and `person.expected_retirement_age` return
    # `InstanceProperty` objects, which are also `Producer` objects.
    years_to_retirement = person.retirement_age - person.age
    response = select(person.name, years_to_retirement)

print(response.results)
# Output:
#     name   v
# 0   Fred  26
# 1  Wilma  26
```

#### See Also

[`Producer.__add__()`](#producer__add__),
[`Producer.__mul__()`](#producer__mul__),
and [`Producer.__truediv__()`](#producer__truediv__).

### `Producer.__rsub__()`

```python
Producer.__rsub__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the difference between the `Producer` values and `other`.
`.__rsub__()` is implemented so that you may use a non-`Producer` object as the left operand.

#### See Also

[`Producer.__sub__()`](#producer__mul__)

### `Producer.__truediv__()`

```python
Producer.__truediv__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the quotient of the `Producer` values and `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

A `Producer` object may be divided by a numeric literal:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    percent_life_completed = person.age / 76
    response = select(person.name, percent_life_completed)

print(response.results)
# Output:
#     v
#     name         v
# 0   Fred  0.513158
# 1  Wilma  0.473684
```

You may also divide two `Producer` objects:

```python
with model.rule():
    fred = Person(name="Fred")
    fred.set(savings=200.0, savings_goal=1000.0)

with model.rule():
    wilma = Person(name="Wilma")
    wilma.set(savings=300.0, savings_goal=500.0)

with model.query() as select:
    person = Person()
    # `person.savings`, and `person.savings_goal`return
    # `InstanceProperty` objects, which are also `Producer` objects.
    percent_goal_completed = savings / savings_goal
    response = select(person.name, percent_goal_completed)

print(response.results)
# Output:
#     name    v
# 0   Fred  0.2
# 1  Wilma  0.6
```

#### See Also

[`Producer.__add__()`](#producer__add__),
[`Producer.__mul__()`](#producer__mul__),
and [`Producer.__sub__()`](#producer__sub__).

### `Producer.__rtruediv__()`

```python
Producer.__rtruediv__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that produces the quotient of the `Producer` values and `other`.
`.__rtruediv__()` is implemented so that you may use a non-`Producer` object as the left operand.

#### See Also

[`Producer.__truediv__()`](#producer__add__)

### `Producer.__gt__()`

```python
Producer.__gt__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) object that restricts the values
represented by the `Producer` object to the values that are strictly greater than `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__gt__()` method is called when you use the `>` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are strictly greater
    # than 36. `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age > 36
    response = select(person.name, person.age)

print(response.results)
# Output:
#    name  age
# 0  Fred   39
```

You may use `>` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age > person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#    name  name2
# 0  Fred  Wilma
```

#### See Also

[`Producer.__ge__()`](#producer__ge__),
[`Producer.__lt__()`](#producer__lt__),
and [`Producer.__le__()`](#producer__le__).

### `Producer.__ge__()`

```python
Producer.__ge__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that restricts `Producer` to values greater than or equal to `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__ge__()` method is called when you use the `>=` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are greater than or equal
    # to 36. `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age >= 36
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name  age
# 0   Fred   39
# 1  Wilma   36
```

You may use `>=` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age > person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#    name  name2
# 0  Fred  Wilma
```

#### See Also

[`Producer.__gt__()`](#producer__gt__),
[`Producer.__lt__()`](#producer__lt__),
and [`Producer.__le__()`](#producer__le__).

### `Producer.__lt__()`

```python
Producer.__lt__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that restricts `Producer` to values strictly less than `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__lt__()` method is called when you use the `<` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are strictly less
    # than 39. `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age < 39
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name  age
# 0  Wilma   36
```

You may use `<` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age < person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#     name  name2
# 0  Wilma  Fred
```

#### See Also

[`Producer.__gt__()`](#producer__gt__),
[`Producer.__ge__()`](#producer__ge__),
and [`Producer.__le__()`](#producer__le__).

### `Producer.__le__()`

```python
Producer.__le__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that restricts `Producer` to values less than or equal to `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__le__()` method is called when you use the `<=` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are greater than or equal
    # to 36. `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age <= 39
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name  age
# 0   Fred   39
# 1  Wilma   36
```

You may use `<=` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age <= person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#     name  name2
# 0  Wilma  Fred
```

#### See Also

[`Producer.__gt__()`](#producer__gt__),
[`Producer.__ge__()`](#producer__ge__),
and [`Producer.__lt__()`](#producer__lt__).

### `Producer.__eq__()`

```python
Producer.__eq__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that restricts `Producer` to values equal to `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__eq__()` method is called when you use the `==` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are equal to 36.
    # `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age == 36
    response = select(person.name, person.age)

print(response.results)
# Output:
#     name  age
# 0  Wilma   36
```

You may use `==` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age == person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#     name  name2
# 0   Fred   Fred
# 1  Wilma  Wilma
```

#### See Also

[`Producer.__ne__()`](#producer__ne__)

### `Producer.__ne__()`

```python
Producer.__ne__(other: Any) -> Expression
```

Returns an [`Expression`](./Expression.md) that restricts `Producer` to values not equal to `other`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `other` | `Any` | A numeric value or another `Producer` object. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

The `Producer.__ne__()` method is called when you use the `!=` operator with a `Producer` object:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person.age` to values that are equal to 36.
    # `person.age` returns an `InstanceProperty` object,
    # which is also a `Producer` object.
    person.age != 36
    response = select(person.name, person.age)

print(response.results)
# Output:
#    name  age
# 0  Fred   39
```

You may use `!=` with two `Producer` objects:

```python
with model.query() as select:
    person1, person2 = Person(), Person()
    person1.age != person2.age
    response = select(person1.name, person2.name)

print(response.results)
# Output:
#     name  name2
#     name  name2
# 0   Fred  Wilma
# 1  Wilma   Fred
```

#### See Also

[`Producer.__eq__()`](#producer__eq__)

### `Producer.__enter__()`

```python
Producer.__enter__() -> None
```

`Producer` objects can be used as [context managers](https://docs.python.org/3/glossary.html#term-context-manager)
in a [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#with)
to apply restrictions in a [rule](./Model.md#modelrule) or [query](./Model.md#modelquery) conditionally.
In a `with` statement, Python calls the context manager's `.__enter__()` method before executing the `with` block.
After the `with` block executes,
the `with` statement automatically executes the [`Producer.__exit__()`](#producer__exit__) method.

#### Returns

`None`

#### Example

You may use `Producer` objects in a `with` statement to set a property or Type conditionally:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")
Adult = model.Type("Adult")

with model.rule():
    Person.add(name="Fred", age=39)
    Person.add(name="Wilma", age=36)
    Person.add(name="Pebbles", age=6)

# People who 18 years old or older are adults.
with model.rule():
    person = Person()
    with person.age >= 18:
        person.set(Adult)

with model.query() as select:
    adult = Adult()
    response = select(adult.name, adult.age)

print(response.results)
# Output:
#     name  age
# 0   Fred   39
# 1  Wilma   36
```

The `with person.age >= 18` block temporarily restricts `person.age` to values greater than or equal to 18.
After Python executes the `with` block, the [`Producer.__exit__()`](#producer__exit__) method is called to remove the restriction.
This allows you to write multiple conditional `with` statements
in the same [rule](./Model.md#modelrule) or [query](./Model.md#modelquery):

```python
Child = model.Type("Child")

with model.rule():
    person = Person()
    with person.age >= 18:
        person.set(Adult)
    with person.age < 18:
        person.set(Child)

with model.query() as select:
    child = Child()
    response = select(child.name, child.age)

print(response.results)
# Output:
#       name  age
# 0  Pebbles    6
```

#### See Also

[`Producer.__exit__()`](#producer__exit__)

### `Producer.__exit__()`

```python
Producer.__exit__() -> None
```

`Producer` objects can be used as [context managers](https://docs.python.org/3/glossary.html#term-context-manager)
in a [`with` statement](https://docs.python.org/3/reference/compound_stmts.html#with)
to apply restrictions in a [rule](./Model.md#modelrule) or [query](./Model.md#modelquery) conditionally.
In a `with` statement, Python calls the context manager's [`.__enter__()`](#producer__enter__)
method before executing the `with` block.
After the `with` block executes, the `with` statement automatically executes the `.__exit__()` method.

See [`Producer.__enter__()`](#producer__enter__) for more information.

#### Returns

`None`

#### See Also

[`Producer.__enter__()`](#producer__enter__)

### `Producer.__getattribute__()`

```python
Producer.__getattribute__(name: str) -> InstanceProperty | None
```

Restricts the values produced to those for which a property named `name` is set
and returns an [`InstanceProperty`](./InstanceProperty.md) object.
`.__getattribute__()` is called whenever you access a property using dot notation, such as `book.title`, or `person.age`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `name` | `str` | The name of the property to get. |

#### Returns

An [`InstanceProperty`](./InstanceProperty.md) object,
except for [`Expression`](./Expression.md) objects, in which case `.__getattribute__()` returns `None`.

#### Example
It is essential to keep in mind that property access adds a constraint to your context.
For example, the following query only returns objects in `Person` that have a `name` _and_ `age` property:

```python
# Add a person with an age property.
with model.rule():
    Person.add(name="Wilma", age=36)

with model.query() as select:
    person = Person()
    # Restrict `person` to objects with an `age` property.
    person.age
    response = select(person.name)

# Fred is not included in the results because he has no `age` property.
print(response.results)
# Output:
#     name
# 0  Wilma
```

#### See Also

[`InstanceProperty`](./InstanceProperty.md)
