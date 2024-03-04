<!-- markdownlint-disable MD024 -->

# Instance

Instances are [producers](./Producer.md) that produce the internal IDs of objects in a model.
You create instances by calling a [`Type`](./Type.md) object or the [`Model.Vars()`](./Model.md#modelvars) method,
which both return an instance of the `Instance` class.

```python
class Instance(model: Model)
```

`Instance` is a subclass of [`Producer`](./Producer.md).

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](./Model.md) | The model in which the instance is created. |

## Example

Use [`Type`](./Type.md) objects and [`Model`](./Model.md) methods to create an `Instance` object
rather than constructing one directly:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    # The `Type.add()` method returns an `Instance` object.
    kermit = Person.add(name="Kermit")
    # `Instance` objects have a `.set()` method for setting properties.
    kermit.set(favorite_color="green")

with model.query() as select:
    # Calling a `Type` object returns an `Instance` object.
    person = Person()
    response = select(person.name)

print(response.results)
# Output:
#      name
# 0  Kermit
```

The following all return `Instance` objects:

- [`Type.add()`](./Type.md#typeadd)
- [`Type.__call__()`](./Type.md#type__call__)
- [`Model.Vars()`](./Model.md#modelvars)

## Attributes and Methods

### `Instance.persist()`

```python
Instance.persist(*args, **kwargs) -> Instance
```

Persists types and properties on an object and returns the persisted `Instance`.
`.persist()` is not typically used and should only be called by advanced users.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](./Type.md) | The type(s) to which the `Instance` is persisted. |
| `*kwargs` | `Any` | Properties and values to persist on the `Instance`. |

#### Returns

And `Instance` object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    fred = Person.add(name="Fred")
    fred.persist(favorite_color="green")
```

A `Person` object with a `favorite_color` property set to `"green"` persists in the model
even if you delete the [rule](./Model.md#modelrule) that adds it.
You may remove persisted object properties using [`Instance.unpersist()`](#instanceunpersist).

#### See Also

[`Instance`](#instanceunpersist)

### `Instance.set()`

```python
Instance.set(*args, **kwargs) -> Instance
```

Sets types and properties on an `Instance` object and returns the `Instance`.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](./Type.md) | The type(s) to which the `Instance` belongs. |
| `*kwargs` | `Any` | Properties and values to set on the `Instance`. |

#### Returns

An `Instance` object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    fred = Person.add(name="Fred")
    fred.set(favorite_color="green", favorite_food="pizza")
```

The rule in the preceding example adds an object identified by the name `"Fred"` to the model and sets
a `favorite_color` property to the string `"green"` and a `favorite_food` property to the string `"pizza"`.

You set object properties with [`Type.add()`](./Type.md#typeadd) and `Instance.set()`.
The difference is that properties set by `Type.add()` uniquely identify the object.

`.set()` returns an `Instance`, which means you may chain calls to `.set()` to add multiple property values:

```python
with model.rule():
    fred = Person.add(name="Fred")
    fred.set(favorite_color="green").set(favorite_color="blue")
```

This version of the rule sets two values to the `favorite_color` property.
Setting a new value on a property does not override existing values.

#### See Also

[`Type.add()`](./Type.md#typeadd)

### `Instance.unpersist()`

```python
Instance.unpersist(*args, **kwargs) -> Instance
```

Unpersists types and properties on objects set with [`.persist()`](#instancepersist) and returns the unpersisted `Instance`.
`.unpersist()` is not typically used and should only be called by advanced users.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*args` | [`Type`](./Type.md) | The type(s) to remove from the `Instance`. |
| `*kwargs` | `Any` | Property values to remove from the `Instance`. |

#### Returns

An `Instance` object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

# Add an object to the `Person` type and persist a
# `favorite_color` property using the `.persist()` method.
with model.rule():
    fred = Person.add(name="Fred")
    fred.persist(favorite_color="green")

# Unpersist the property set in the preceding rule.
with model.rule():
    fred = Person(name="Fred")
    fred.unpersist(favorite_color="green")
```

#### See Also

[`Instance.persist()`](#instancepersist)
