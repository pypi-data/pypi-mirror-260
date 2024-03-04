<!-- markdownlint-disable MD024 -->

# `Aggregates`

The `Aggregates` class serves as a namespace for aggregate methods.
You do not create `Aggregates` objects directly.
They are automatically instantiated when you create a [`Model`](./Model.md).
You access a model's `Aggregates` object via the [`Model.aggregates`](./Model.md#modelaggregates) attribute.

```python
class Aggregates(model: Model)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model for which the `Aggregates` object is created. |

## Example

```python
import relationalai as rai

model = rai.Model("myModel")

# `model.aggregates` is an `Aggregates` object.
print(type(model.aggregates))
# Output:
# <class 'relationalai.dsl.Aggregates'>
```

A model's `Aggregates` object contains methods to create [`Expression`](./Expression.md) objects
that aggregate values from one or more [`Producer`](./Producer.md) objects.

For example, the [`Aggregates.count()`](#aggregatescount) method returns an `Expression`
that counts the number of values produced by a `Producer`:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe")
    Person.add(name="Jane")

with model.query() as select:
    person = Person()
    person_count = model.aggregates.count(person)
    response = select(person_count)

print(response.results)
# Output:
#    v
# 0  2
```

## Attributes and Methods

### `Aggregates.avg()`

```python
Aggregates.avg(*args: Producer, per: Optional[List[Producer]]) -> Expression
```

Creates an [`Expression`](./Expression.md) object that produces the average of
the values produced by a [`Producer`](./Producer.md).
Pass a list of one or more `Producer` objects to the optional `per` parameter
to group values and compute the average per group.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Producer`](./Producer.md) | One or more [`Producer`](./Producer.md) objects. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)

with model.query() as select:
    person = Person()
    avg_age = model.aggregates.avg(person.age)
    response = select(avg_age)

print(response.results)
# Output:
#       v
# 0  40.0
```

`person.age` represents the _set_ of all ages in the model.
If two people have the same age, you must pass the `person` instance,
in addition to `person.age`, to `.avg()` so that each person contributes to the average:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)
    Person.add(name="John", age=41)

with model.query() as select:
    person = Person()
    avg_age = model.aggregates.avg(person, person.age)
    response = select(avg_age)

print(response.results)
# Output:
#            v
# 0  39.666667
```

When the [query](./Model.md#modelquery) is evaluated,
all pairs of `person` objects and their `age` properties are produced, and the average of the age values is computed.
You may pass any number of [`Producer`](./Producer.md) objects to `.avg()`.
The aggregation occurs over the values produced by the last argument.

To group values and compute the average for each group,
pass one or more `Producer` objects to the optional `per` parameter as a list.
In the following example, the `person` object is passed to `per` to compute the average age of a person's friends:

```python
import relationalai as rai

model = rai.Model("friends")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe", age=41)
    jane = Person.add(name="Jane", age=39)
    john = Person.add(name="John", age=41)
    joe.set(friend=jane).set(friend=john)
    jane.set(friend=joe)
    john.set(friend=joe)

avg = model.aggregates.avg
with model.query() as select:
    person = Person()
    avg_friend_age = avg(person.friend, person.friend.age, per=[person])
    response = select(person.name, avg_friend_age)

print(response.results)
# Output:
#    name     v
# 0  Jane  41.0
# 1   Joe  40.0
# 2  John  41.0
```

#### See Also

[`Aggregates.count()`](#aggregatescount) and [`Aggregates.sum()`](#aggregatessum).

### `Aggregates.count()`

```python
Aggregates.count(*args: Producer, per: Optional[List[Producer]]) -> Expression
```

Creates an [`Expression`](./Expression.md) object that counts the number of values a [Producer](./Producer.md) produces.
Pass a list of one or more `Producer` objects to the optional `per` parameter to group values and count each group.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Producer`](./Producer.md) | One or more [`Producer`](./Producer.md) objects. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)
    Person.add(name="John", age=41)

with model.query() as select:
    person = Person()
    num_people = model.aggregates.count(person)
    response = select(num_people)

print(response.results)
# Output:
#    v
# 0  3
```

Take care when counting properties that may have multiple values.
`.count()` counts the number of unique values represented by a `Producer`.
For instance, there are two age values, not three, since two people are the same age:

```python
with model.query() as select:
    person = Person()
    num_ages = model.aggregates.count(person.age)
    response = select(num_ages)

print(response.results)
# Output:
#    v
# 0  2
```

You may pass multiple `Producer` objects to `.count()`:

```python
with model.query() as select:
    person = Person()
    num_person_age_pairs = model.aggregates.count(person, person.age)
    response = select(num_person_age_pairs)

print(response.results)
# Output:
#    v
# 0  3
```

When you pass both `person` and `person.age`, `.count()` counts the number of _pairs_ of people and their ages.
`.count()` supports any number of arguments.

To group values and count the number of values in each group,
pass one or more `Producer` objects to the optional `per` parameter as a list.
In the following example, the `person` object is passed to `per` to count the number of friends each person has:

```python
import relationalai as rai

model = rai.Model("friends")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe")
    jane = Person.add(name="Jane")
    john = Person.add(name="John")
    joe.set(friend=jane).set(friend=john)
    jane.set(friend=joe)
    john.set(friend=joe)

with model.query() as select:
    person = Person()
    friend_count = model.aggregates.count(person.friend, per=[person])
    response = select(person.name, friend_count)

print(response.results)
# Output:
#    name  v
# 0  Jane  1
# 1   Joe  2
# 2  John  1
```

#### See Also

[`Aggregates.avg()`](#aggregatesavg) and [`Aggregates.sum()`](#aggregatessum).

### `Aggregates.rank_asc()`

```python
Aggregates.rank_asc(*args: Producer, per: Optional[List[Producer]]) -> Expression
```

Creates an [`Expression`](./Expression.md) object that produces the
ascending sort order of the values produced by a [`Producer`](./Producer.md).
Pass a list of one or more `Producer` objects to the optional `per` parameter to group and sort values.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Producer`](./Producer.md) | One or more [`Producer`](./Producer.md) objects. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)

with model.query() as select:
    person = Person()
    rank = model.aggregates.rank_asc(person.age)
    response = select(rank, person.name, person.age)

print(response.results)
# Output:
#    v  name  age
# 0  1  Jane   39
# 1  2   Joe   41
```

`person.age` represents the _set_ of all ages in the model.
If two people have the same age, you must pass the `person` instance,
in addition to `person.age`, to `.rank_asc()` so that each person contributes to the average:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)
    Person.add(name="John", age=41)

with model.query() as select:
    person = Person()
    rank = model.aggregates.rank_asc(person.age, person)
    response = select(rank, person.name, person.age)

print(response.results)
# Output:
#    v  name  age
# 0  1  Jane   39
# 1  2  John   41
# 2  3   Joe   41
```

When the [query](./Model.md#modelquery) is evaluated,
all pairs of `person` objects and their `age` properties are sorted.
You may pass any number of [`Producer`](./Producer.md) objects to `.rank_asc()`,
which sorts the set of values in ascending [lexicographic order](https://en.wikipedia.org/wiki/Lexicographic_order)
by column.

To group values and compute the average for each group,
pass one or more `Producer` objects as a list to the optional `per` parameter.
In the following example, the `person` object is passed to `per` to sort each person's friends by age:

```python
import relationalai as rai

model = rai.Model("friends")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe", age=41)
    jane = Person.add(name="Jane", age=39)
    john = Person.add(name="John", age=41)
    joe.set(friend=jane).set(friend=john)
    jane.set(friend=joe)
    john.set(friend=joe)

rank_asc = model.aggregates.rank_asc
with model.query() as select:
    person = Person()
    friend_rank = rank_asc(person.friend.age, person.friend, per=[person])
    response = select(
        person.name, friend_rank, person.friend.name, person.friend.age
    )

print(response.results)
# Output:
#    name  v name2  age
# 0  Jane  1   Joe   41
# 1   Joe  1  Jane   39
# 2   Joe  2  John   41
# 3  John  1   Joe   41
```

#### See Also

[`Aggregates.rank_desc()`](#aggregatesrank_desc).

### `Aggregates.rank_desc()`

```python
Aggregates.rank_desc(*args: Producer, per: Optional[List[Producer]]) -> Expression
```

Creates an [`Expression`](./Expression.md) object that represents the sort order
of the values represented by the [`Producer`](./Producer.md) objects passed to `args` in descending order.
Pass a list of one or more `Producer` objects to the optional `per` parameter to group and sort values.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Producer`](./Producer.md) | One or more [`Producer`](./Producer.md) objects. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)

with model.query() as select:
    person = Person()
    rank = model.aggregates.rank_desc(person.age)
    response = select(rank, person.name, person.age)

print(response.results)
# Output:
#    v  name  age
# 0  1   Joe   41
# 1  2  Jane   39
```

`person.age` represents the _set_ of all ages in the model.
If two people have the same age, you must pass the `person` instance,
in addition to `person.age`, to `.rank_desc()` so that each person contributes to the average:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)
    Person.add(name="John", age=41)

with model.query() as select:
    person = Person()
    rank = model.aggregates.rank_desc(person.age, person)
    response = select(rank, person.name, person.age)

print(response.results)
# Output:
#    v  name  age
# 0  1   Joe   41
# 1  2  John   41
# 2  3  Jane   39
```

When the [query](./Model.md#modelquery) is evaluated,
all pairs of `person` objects and their `age` properties are sorted.
You may pass any number of [`Producer`](./Producer.md) objects to `.rank_desc()`,
which sorts the set of values in descending [lexicographic order](https://en.wikipedia.org/wiki/Lexicographic_order)
by column.

To group values and compute the average for each group,
pass one or more `Producer` objects as a list to the optional `per` parameter.
In the following example, the `person` object is passed to `per` to sort each person's friends by age:

```python
import relationalai as rai

model = rai.Model("friends")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe", age=41)
    jane = Person.add(name="Jane", age=39)
    john = Person.add(name="John", age=41)
    joe.set(friend=jane).set(friend=john)
    jane.set(friend=joe)
    john.set(friend=joe)

rank_desc = model.aggregates.rank_desc
with model.query() as select:
    person = Person()
    friend_rank = rank_desc(person.friend.age, person.friend, per=[person])
    response = select(
        person.name, friend_rank, person.friend.name, person.friend.age
    )

print(response.results)
# Output:
#    name  v name2  age
# 0  Jane  1   Joe   41
# 1   Joe  1  John   41
# 2   Joe  2  Jane   39
# 3  John  1   Joe   41
```

#### See Also

[`Aggregates.rank_desc()`](#aggregatesrank_desc).

### `Aggregates.sum()`

```python
Aggregates.sum(*args: Producer, per: Optional[List[Producer]]) -> Expression
```

Creates an [`Expression`](./Expression.md) object that produces the sum of the values produced by a [`Producer`](./Producer.md).
Pass a list of one or more `Producer` objects to the optional `per` parameter to group values and compute the sum per group.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Producer`](./Producer.md) | One or more [`Producer`](./Producer.md) objects. |

#### Returns

An [`Expression`](./Expression.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)

with model.query() as select:
    person = Person()
    age_sum = model.aggregates.sum(person.age)
    response = select(age_sum)

print(response.results)
# Output:
#     v
# 0  80
```

`person.age` represents the _set_ of all ages in the model.
If two people have the same age, you must pass the `person` instance,
in addition to `person.age`, to `.sum()` so that each person contributes to the sum:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)
    Person.add(name="John", age=41)

with model.query() as select:
    person = Person()
    age_sum = model.aggregates.sum(person, person.age)
    response = select(age_sum)

print(response.results)
# Output:
#      v
# 0  121
```

When the [query](./Model.md#modelquery) is evaluated,
all pairs of `person` objects and their `age` properties are formed, and the sum of the age values is computed.
You may pass any number of [`Producer`](./Producer.md) objects to `.sum()`.
The aggregation occurs over the values produced by the last argument.

To group values and compute the sum for each group,
pass one or more `Producer` objects to the optional `per` parameter as a list.
In the following example, the `person` object is passed to `per` to compute the sum of the ages of a person's friends:

```python
import relationalai as rai

model = rai.Model("friends")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe", age=41)
    jane = Person.add(name="Jane", age=39)
    john = Person.add(name="John", age=41)
    joe.set(friend=jane).set(friend=john)
    jane.set(friend=joe)
    john.set(friend=joe)

sum_ = model.aggregates.sum
with model.query() as select:
    person = Person()
    friend_age_sum = sum_(person.friend, person.friend.age, per=[person])
    response = select(person.name, friend_age_sum)

print(response.results)
# Output:
#    name   v
# 0  Jane  41
# 1   Joe  80
# 2  John  41
```

#### See Also

[`Aggregates.avg()`](#aggregatesavg) and [`Aggregates.count()`](#aggregatescount).
