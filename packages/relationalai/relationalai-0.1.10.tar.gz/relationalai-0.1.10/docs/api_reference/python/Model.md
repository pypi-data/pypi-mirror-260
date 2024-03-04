<!-- markdownlint-disable MD024 -->

# `Model`

Models represent collections of [objects](./Instance.md).
Objects, like Python objects, have [types](./Type.md) and [properties](./InstanceProperty.md).
Objects may have multiple types, and properties may have multiple values.
You write [rules](./Model.md#modelrule) to describe objects in your model and the relationships between them
and write [queries](./Model.md#modelquery) to extract data from your model.

Models are instances of the `Model` class.

```python
class relationalai.Model(name: str)
```

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `name` | `str` | The name of the model. Must be at least three characters and must begin with a Unicode letter or underscore, followed by any number of of Unicode letters, numbers, underscores, or hyphens. |

## Example

```python
import relationalai as rai

# Create a new model.
model = rai.Model("myModel")
```

## Attributes and Methods

### `Model.aggregates`

Returns an [`Aggregates`](./Aggregates.md) object for access to aggregate methods.

#### Example

A model's [`Aggregates`](./Aggregates.md) object contains methods to create [`Expression`](./Expression.md) objects
that aggregate values from one or more [`Producer`](./Producer.md) objects:

```python
import relationalai as rai

model = rai.Model("pets")
Person = model.Type("Person")
Dog = model.Type("Dog")
Bird = model.Type("Bird")

with model.rule():
    joe = Person.add(name="Joe")
    buddy = Dog.add(name="Buddy")
    miles = Dog.add(name="Miles")
    joe.set(pet=buddy).set(pet=miles)

with model.rule():
    jane = Person.add(name="Jane")
    mr_beaks = Bird.add(name="Mr. Beaks")
    jane.set(pet=mr_beaks)

# How many pets does each person have?
with model.query() as select:
    person = Person()
    pet_count = model.aggregates.count(person.pet, per=[person])
    response = select(person.name, pet_count)

print(response.results)
# Output:
#    name  v
# 0  Jane  1
# 1   Joe  2
```

#### See Also

[`Aggregates`](./Aggregates.md)

### `Model.alias()`

```python
Model.alias(ref: Producer, name: str) -> Var
```

Rename `ref` so that it appears with the alias `name` in results.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `ref` | [`Producer`](./Producer.md) | The object to be aliased. |
| `name` | `str` | The name to use as the alias. |

#### Returns

A `Var` object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe")

with model.query() as select:
    person = Person()
    response = select(person.name)

print(response.results)
# Output:
#     name  <-- Column name is the property name
# 0   Alex

# You can change the default column name with `.alias()`.
with model.query() as select:
    person = Person()
    response = select(model.alias(person.name, "my_col"))

print(response.results)
# Output:
#     my_col
# 0     Alex
```

### `Model.found()`

```python
Model.found(dynamic: bool = False) -> Context
```

Creates a [`Context`](./Context.md) that restricts [producers](./Producer.md) in a [rule](#modelrule)
or [query](#modelquery) to only those for which the conditions in the `.found()` context hold.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](Context.md) object.

#### Example

`Model.found()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
It must be called from within a [rule](#modelrule) or [query](#modelquery) context:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=22)
    Person.add(name="Janet", age=63)

# `model.found()` is always called in a nested `with` block
# inside of a `model.rule()` or `model.query()` context.
with model.query() as select:
    person = Person()
    with model.found():
        person.age > 60
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0  Janet
```

In the preceding example, `model.found()` restricts the `person` instance to objects with an `age` value greater than 60.
But it does so without exposing the `person.age` producer to the surrounding context.
In other words, the restriction of `person.age` to values greater than 60 only applies inside of the `model.found()` sub-context.

This is especially important to remember when objects have a property with multiple values:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")
Dog = model.Type("Dog")
Bird = model.Type("Bird")

# Add people and pets to the model.
with model.rule():
    fred = Person.add(name="Fred", age=22)
    janet = Person.add(name="Janet", age=63)
    mr_beaks = Bird.add(name="Mr. Beaks")
    spot = Dog.add(name="Spot")
    buddy = Dog.add(name="Buddy")
    # Fred has one pet and Janet has two.
    fred.set(pet=buddy)
    janet.set(pet=spot).set(pet=mr_beaks)

# What are the names of all pets of bird owners?
with model.query() as select:
    person = Person()
    # Restrict `person` to objects with a `pet` property
    # set to an object in the `Bird` type.
    with model.found():
        person.pet == Bird()
    response = select(person.name, person.pet.name)

print(response.results)
# Output:
#     name      name2
# 0  Janet  Mr. Beaks
# 1  Janet       Spot
```

Janet is the only person in the results because she is the only person with a pet bird.
Both of her pets, Spot and Mr. Beaks, appear in the results because the restriction
of `person.pet` to the `Bird` type only applies inside the `with model.found()` block.

Contrast that to the following query:

```python
with model.query() as select:
    person = Person()
    person.pet == Bird()
    response = select(person.name, person.pet.name)

print(response.results)
# Output:
#     name      name2
# 0  Janet  Mr. Beaks
```

Only Mr. Beaks appears because `person.pet == Bird()` restricts `person.pet` to the `Bird` type.

#### See Also

[`Context`](./Context.md) and [`Model.not_found()`](#modelnot_found)

### `Model.name`

Returns the model name.

#### Example

```python
import relational as rai

model = rai.model("myModel")

print(model.name)
# Output:
# 'myModel'
```

### `model.not_found()`

```python
Model.not_found(dynamic: bool = False) -> Context
```

Creates a [`Context`](./Context.md) that restricts [producers](./Producer.md) in a [rule](#modelrule) or [query](#modelquery)
to only those values for which any of the conditions in the `.not_found()` context fail.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](Context.md) object.

#### Example

`Model.not_found()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
It must be called from within a [rule](#modelrule) or [query](#modelquery) context:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Fred", age=22)
    Person.add(name="Janet", age=63)

# `model.not_found()` is always called in a nested `with` block
# inside of a `model.rule()` or `model.query()` context.
with model.query() as select:
    person = Person()
    # Restrict `person` to objects that do not have
    # a `name` property set to the string `"Janet"`.
    with model.not_found():
        person.name == "Janet"
    response = select(person.name)

print(response.results)
# Output:
#    name
# 0  Fred
```

#### See Also

[`Context`](./Context.md) and [`model.found()`](#modelfound)

### `Model.ordered_choice()`

```python
Model.ordered_choice(dynamic: bool = True) -> Context
```

Creates a [`Context`](./Context.md) that applies consecutive `with` blocks in an "if-else" fashion.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](Context.md) object.

#### Example

`Model.ordered_choice()` is a
[context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
It must be called from within a [rule](#modelrule) or [query](#modelquery) context:

```python
import relationalai as rai

model = rai.Model("students")
Student = model.Type("Student")

with model.rule():
    Student.add(name="Fred", grade=87)
    Student.add(name="Johnny", grade=65)
    Student.add(name="Mary", grade=98)

# `model.ordered_choice()` is always called in a nested `with` block
# inside of a `model.rule()` or `model.query()` context.
with model.rule():
    student = Student()
    # Set a `letter_grade` property on students whose value
    # depends on their `.grade` property. Note that only `with`
    # statements are allowed inside of a `Model.ordered_choice()` context.
    with model.ordered_choice():
        with student.grade >= 90:
            # A `with` block may contain any valid query builder code.
            student.set(letter_grade="A")
        with student.grade >= 80:
            student.set(letter_grade="B")
        with student.grade >= 70:
            student.set(letter_grade="C")
        with student.grade < 70:
            student.set(letter_grade="F")

# Which students got a B?
with model.query() as select:
    student = Student(letter_grade="B")
    response = select(student.name, student.grade, student.letter_grade)

print(response.results)
# Output:
#    name  grade letter_grade
# 0  Fred     87            B
```

The [`Model.ordered_choice().__enter__()`](./Context.md#context__enter__) method
returns a [`ContextSelect`](./ContextSelect.md) object that you may use to choose objects and set properties
in a query instead of a rule.
For instance, the following example calculates letter grades in a query instead of setting them as object properties:

```python
import relationalai as rai

model = rai.Model("students")
Student = model.Type("Student")

with model.rule():
    Student.add(name="Fred", grade=87)
    Student.add(name="Johnny", grade=65)
    Student.add(name="Mary", grade=98)

# Which students got a B?
with model.query() as select:
    student = Student()
    with model.ordered_choice() as students:
        with student.grade >= 90:
            students.add(student, letter_grade="A")
        with student.grade >= 80:
            students.add(student, letter_grade="B")
        with student.grade >= 70:
            students.add(student, letter_grade="C")
        with student.grade < 70:
            students.add(student, letter_grade="F")

    students.letter_grade == "B"
    response = select(students.name, students.grade, students.letter_grade)

print(response.results)
# Output:
#    name  grade  v
# 0  Fred     87  B
```

Only `with` statements are allowed inside of a `Model.ordered_choice()` context.
Creating [instances](./Instance.md) and other [producers](./Producer.md) will result in an error:

```python
with model.rule():
    with model.ordered_choice():
        # THIS IS NOT ALLOWED:
        student = Student()

        # ...
```

Think of consecutive `with` statements inside of a `Model.ordered_choice()` context as branches of an `if`-`else` statement.
The preceding example sets a `letter_grade` property on `student` objects,
the value of which depends on the student's `grade` property.
Only values from the first matching `with` statement are set.

Compare that to the same sequence of `with` statements written outside of a `Model.ordered_choice()` context:

```python
with model.rule():
    student = Student()
    with student.grade >= 90:
        student.set(letter_grade="A")
    with student.grade >= 80:
        student.set(letter_grade="B")
    with student.grade >= 70:
        student.set(letter_grade="C")
    with student.grade < 70:
        student.set(letter_grade="F")

# Which students got a B?
with model.query() as select:
    student = Student(letter_grade="B")
    response = select(student.name, student.grade, student.letter_grade)

print(response.results)
# Output:
#    name  grade letter_grade
# 0  Fred     87            B
# 1  Mary     98            B
```

Mary has `.letter_grade` set to `"B"`.
She _also_ has `.letter_grade` set to `"A"` and `"C"` because her grade meets the conditions
in the first three of the four `with` statements.

#### See Also

[`Context`](./Context.md),
[`ContextSelect`](./ContextSelect.md),
and [`Model.union()`](#modelunion).

### `Model.query()`

```python
Model.query(dynamic: bool = False) -> Context
```

Creates a query [`Context`](./Context.md).

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the query is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](./Context.md) object.

#### Example

`Model.query()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
Use the `as` part of the `with` statement to assign the [`ContextSelect`](./ContextSelect.md) object
created by `Model.query()` to a variable named `select` so that you may select query results:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

# Add people to the model.
with model.rule():
    alex = Person.add(name="Alex", age=19)
    bob = Person.add(name="Bob", age=47)
    carol = Person.add(name="Carol", age=17)

# A `with model.query() as select` block begins a new query.
# `select` is a `ContextSelect` object used to select query results.
with model.query() as select:
    person = Person()
    response = select(person.name)

print(response.results)
# Output:
#     name
# 0   Alex
# 1    Bob
# 2  Carol
```

You write queries using RelationalAI's declarative query builder syntax.
See [Getting Started with RelationalAI](../../getting_started.md) for an introduction to writing queries.

Note that you may pass data from your Python application into a query:

```python
name_to_find = "Carol"
property_to_find = "age"

with model.query() as select:
    person = Person(name=name_to_find)
    prop = getattr(person, property_to_find)
    response = select(prop)

print(response.results)
# Output:
#    age
# 0   17
```

Here, the Python variables `name_to_find` and `property_to_find` are used directly in the query.
Python's built-in [`getattr()`](https://docs.python.org/3/library/functions.html#getattr) function
gets the `person` property with the name `property_to_find`.

By default, queries do not support `while` and `for` loops and other flow control tools such as `if` and
[`match`](https://docs.python.org/3/tutorial/controlflow.html#match-statements).
You can enable flow control by setting the `dynamic` parameter to `True`,
which lets you use Python flow control as a macro to build up a query dynamically:

```python
# Application is being used by an external user.
IS_INTERNAL_USER = FALSE

with model.query() as select:
    person = Person()
    if not IS_INTERNAL_USER:
        Public(person)
    response = select(person.name, person.age)
```

In this query, the application user's state determines whether or not to include a condition.
If the user is external, only `Public` objects are selected.

#### See Also

[`Context`](./Context.md),
[`ContextSelect`](./ContextSelect.md),
and [`Model.rule()`](./Model.md#modelrule).

### `Model.rule()`

```python
Model.rule(dynamic:bool=False) -> Context
```

Creates a rule [`Context`](./Context.md).

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the rule is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](./Context.md) object.

#### Example

`Model.rule()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.

Rules describe objects in a model:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")
Adult = model.Type("Adult")

# Add people to the model.
with model.rule():
    alex = Person.add(name="Alex", age=19)
    bob = Person.add(name="Bob", age=47)
    carol = Person.add(name="Carol", age=17)

# All people that are 18 years old or older are adults.
with model.rule() as select:
    person = Person()
    person.age >= 18
    person.set(Adult)
```

You write rules using RelationalAI's declarative query builder syntax.
See [Getting Started with RelationalAI](../../getting_started.md) for an introduction to writing rules and queries.

Note that you may pass data from your Python application into a rule:

```python
min_adult_age = 21

with model.rule() as select:
    person = Person()
    person.age >= min_adult_age
    person.set(Adult)
```

By default, rules do not support `while` and `for` loops and other flow control tools such as `if` and
[`match`](https://docs.python.org/3/tutorial/controlflow.html#match-statements).
You can enable flow control by setting the `dynamic` parameter to `True`,
which lets you use Python flow control as a macro to build up a rule dynamically:

```python
with model.rule(dynamic=True):
    person = Person()
    for i in range(3):
        person.set(count=i)
```

### `Model.scope()`

```python
Model.scope(dynamic: bool = False) -> Context
```

Creates a sub-[`Context`](./Context.md) that can be used to select objects
without restricting [producers](./Producer.md) in the surrounding context.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](Context.md) object.

#### Example

`Model.scope()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
It must be called from within a [rule](#modelrule) or [query](#modelquery) context:

```python
import relationalai as rai

model = rai.Model("pets")
Person = model.Type("Person")
Dog = model.Type("Dog")
Cat = model.Type("Cat")

with model.rule():
    joe = Person.add(name="Joe")
    whiskers = Cat.add(name="Whiskers")
    miles = Dog.add(name="Miles")
    joe.set(pet=whiskers).set(pet=miles)

    jane = Person.add(name="Jane")
    spot = Cat.add(name="Spot")
    jane.set(pet=spot)

DogOwner = model.Type("DogOwner")
CatOwner = model.Type("CatOwner")

with model.rule():
    person = Person()
    with model.scope():
        # Restrict `person.pet` to `Dog` objects and
        # set the `DogOwner` type on `person`.
        Dog(person.pet)
        person.set(DogOwner)
    # Outside of the `with model.scope()` block, the
    # restriction on `person.pet` no longer applies.
    # `person` represents every person, not just people with pet dogs.
    with model.scope():
        Cat(person.pet)
        person.set(CatOwner)

# Joe is a dog owner.
with model.query() as select:
    dog_owner = DogOwner()
    response = select(dog_owner.name)

print(response.results)
# Output:
#   name
# 0  Joe

# Both Jane and Joe are cat owners.
with model.query() as select:
    cat_owner = CatOwner()
    response = select(cat_owner.name)

print(response.results)
# Output:
#    name
# 0  Jane
# 1   Joe
```

You may also write the above rule more compactly with `.scope()` by using the
[`Producer`](./Producer.md) objects returned by `Dog(person.pet)` and `Cat(person.pet)` as context managers:

```python
with model.rule()
    person = Person()
    with Dog(person.pet):
        person.set(DogOwner)
    with Cat(person.pet)
        person.set(CatOwner)
```

In most cases where you benefit from `Model.scope()`,
you may rewrite the rule or query more compactly using the [`Producer`](./Producer.md) object's context manager support
or one of the built-in context methods, like [`Model.found()`](#modelfound) or [`Model.union()`](#modelunion).

#### See Also

[`Context`](./Context.md),
[`Model.found()`](#modelnot_found),
[`Model.not_found()`](#modelnot_found),
[`Model.ordered_choice()`](#modelordered_choice),
and [`Model.union()`](#modelunion).

### `Model.Type()`

```python
Model.Type(name: str) -> Type
```

Creates a new [Type](./Type.md) in the model.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `name` | `str` | The name of the type. Type names must begin with a Unicode letter or an underscore followed by one or more Unicode letters, underscores, or numbers. |

#### Returns

A [`Type`](./Type.md) object.

#### Example

```python
import relationalai as rai

model = rai.Model("people")

Person = model.Type("Person")
```

#### See Also

[`Type`](./Type.md)

### `Model.union()`

```python
Model.union(dynamic: bool = False) -> Context
```

Creates a [`Context`](./Context.md) used to group objects in a rule or query.

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `dynamic` | `bool` | Whether or not the context is dynamic. Dynamic queries support Python control flow as macros. See [`Context`](./Context.md) for more information. |

#### Returns

A [`Context`](./Context.md) object.

#### Example

`Model.union()` is a [context manager](https://docs.python.org/3/glossary.html#term-context-manager)
and should be called in a `with` statement.
It must be called from within a [rule](#modelrule) or [query](#modelquery) context:

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Alice", age=10)
    Person.add(name="Bob", age=30)
    Person.add(name="Carol", age=60)

# `model.union()` is always called in a nested `with` block
# inside of a `model.rule()` or `model.query()` context.
with model.query() as select:
    person = Person()
    with model.union() as seniors_and_kids:
        # Only `with` statements are allowed directly inside of a `Model.union()` context.
        with person.age >= 60:
            # A `with` block may contain any valid query builder code.
            seniors_and_kids.add(person)
        with person.age < 13:
            seniors_and_kids.add(person)
    response = select(seniors_and_kids.name)

print(response.results)
# Output:
#     name
# 0  Alice
# 1  Carol
```

Here, `seniors_and_kids` is a [`ContextSelect`](./ContextSelect.md) object returned by
the `model.union()` context's `.__enter__()` method when the `with` statement is executed.
It behaves similar to a [`Type`](./Type.md) in the sense that
`seniors_and_kids` is a collection of objects and has an `.add()` method used to add objects to the collection.
Unlike a `Type`, however, `seniors_and_kids` may only have existing objects added to it.
Moreover, the fact that an object is in `seniors_and_kids` is only retained for the lifetime of the query.

You can use `seniors_and_kids` outside of the `model.union()` block that created it.
Accessing a property from `seniors_and_kids` returns an [`InstanceProperty`](./InstanceProperty.md) object that
produces the property values of the objects in the `seniors_and_kids` collection.

You may also add collection-specific properties to objects when they are added to `seniors_and_kids`.
For instance, the following modified query adds a note to each object in the `seniors_and_kids` collection:

```python
with model.query() as select:
    person = Person()
    with model.union() as seniors_and_kids:
        with person.age >= 60:
            seniors_and_kids.add(person, note="senior")
        with person.age < 13:
            seniors_and_kids.add(person, note="kid")
    response = select(seniors_and_kids.name, seniors_and_kids.note)

print(response.results)
# Output:
#     name       v
# 0  Alice     kid
# 1  Carol  senior
```

The `note` property is only accessible from the `seniors_and_kids` object.
Trying to access `person.note` property on `person` will fail,
unless there is already a `note` property for `person` objects.

### `Model.Vars()`

```python
Model.Vars(count: int) -> List[Instance]
```

Creates `count` number of [`Instance`](./Instance.md) objects that represent unknown values
in a [rule](#modelrule) or [query](#modelquery).

#### Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `count` | `int` | The number of `Instance` objects to return. |

#### Returns

An [`Instance`](./Instance.md) object or a `list` of `Instance` objects.

#### Example

You must call `Model.Vars()` from within a [rule](#modelrule) or [query](#modelquery):

```python
import relationalai as rai

model = rai.Model("people")
Person = model.Type("Person")

with model.rule():
    Person.add(name="Joe", age=41)
    Person.add(name="Jane", age=39)

with model.query() as select:
    person = Person()
    x = model.Vars(1)
    person.age == x
    x > 40
    response = select(person.name, x)

print(response.results)
# Output:
#   name   v
# 0  Joe  41
```
