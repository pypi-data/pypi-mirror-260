__all__ = (
    'Object',
    )

from . import constants
from . import dtypes
from . import fields
from . import meta


class Constants(constants.PackageConstants):  # noqa

    pass


@dtypes.dataclass_transform(
    eq_default=True,
    kw_only_default=True,
    field_specifiers=(fields.Field, ),
    )
class Object(meta.Base):  # type: ignore[misc]
    """
    Base Object.

    ---

    Usage
    -----

    * Subclass to create objects for your application.

    General Recommendations
    -----------------------

    * Ideally, objects should be 1:1 with their counterparts in the \
    data store from which they are originally sourced (even \
    if that data store is your own database, and even if that \
    data is not ostensibly stored in a 1:1 manner, as is the case \
    with most relational databases).
        \
        * For example, if there is a SQL table called `pets` \
        with the schema below, you would want to create \
        a corresponding `python representation` similar to \
        the following.

    #### pets table

    ```
    | id  | name     | type   |
    | --- | -------- | ------ |
    | a1  | fido     | dog    |
    | a2  | garfield | cat    |
    | a3  | sophie   | dog    |
    | a4  | stripes  | turtle |
    ```

    #### python representation

    ```py
    import fgr


    class Pet(fgr.Object):
        \"""A pet.\"""

        id_: fgr.Field[str]  # Trailing underscores are special
                             # in fgr, check the documentation
                             # below for more detail.
        name: fgr.Field[str] = 'Fido'  # Setting = 'Fido' will mean that
                                       # all Pet() instances will be
                                       # named 'Fido' by default.
        type: fgr.Field[str]  # You can make a field 'required' by
                              # not specifying a default value.

    ```

    ---

    Special Rules
    -------------

    #### Default Values
    Subclassed (derivative) objects should include default values for \
    all fields specified. In cases where a default value is not specified, \
    `None` will be used instead and the field will be assumed to be \
    'required' for all downstream purposes (ex. as a query parameter \
    for HTTP requests) unless otherwise specified explicitly.

    #### Type Annotations
    Type annotations are required and must be a generic `Field[type]`. \
    For example: `Field[int]`, `Field[str]`, `Field[str | bool]`.

    * Not only is this best practice, these are leveraged downstream \
    to do things like auto-document and auto-generate API's.

    #### Uniform Casing
    ALL Fields must be either camelCase or snake_case, with the only \
    exception being that fields may begin with an underscore '_', so long \
    as all following characters adhere to camelCase or snake_case conventions.

    #### Underscore Prefix for Private Fields
    Fields that begin with an underscore '_' will be ignored on \
    conversion to / from DBO, REST, and JSON representations, \
    unless the field ends with 'id' or 'id_' (case insensitive), \
    in which case it will still be converted.

    * This follows the broader pattern of flagging methods and \
    attributes as private / internal to a system with a preceding \
    underscore. It should be expected that end users of your \
    system will not need to interact with these fields.

    #### Underscore Suffix for Reserved Keyword Fields
    Fields with a trailing underscore '_' will automatically have \
    the trailing underscore removed on conversion to / from \
    DBO, REST, and JSON representations.

    * This allows for python keywords, such as 'in_', to be used \
    as object fields, where they would otherwise raise errors \
    without the proceeding underscore.

    * On translation to and from dictionaries, keys without \
    underscores will still be checked against these fields -- \
    so, a dictionary with key 'in' will correctly map to the 'in_' \
    field on the Object. See below for more detail.

    ```py
    import fgr


    class Pet(fgr.Object):
        \"""A pet.\"""

        id_: fgr.Field[str]
        _alternate_id: fgr.Field[str]

        name: fgr.Field[str]
        type: fgr.Field[str]
        in_: fgr.Field[str]
        is_tail_wagging: fgr.Field[bool] = True


    # This means each of the below will work.
    bob_the_dog = Pet(
        id='abc123',
        _alternate_id='dog1',
        name='Bob',
        type='dog',
        in_='timeout',
        is_tail_wagging=False
        )
    bob_the_dog = Pet(
        {
            'id': 'abc123',
            '_alternate_id': 'dog1',
            'name': 'Bob',
            'type': 'dog',
            'in': 'timeout',
            'is_tail_wagging': False
            }
        )

    # And so would this, since translation
    # automatically handles camelCase to
    # snake_case conversions.
    bob_the_dog = Pet(
        {
            'id': 'abc123',
            'alternateId': 'dog1',
            'name': 'Bob',
            'type': 'dog',
            'in': 'timeout',
            'isTailWagging': False
            }
        )

    ```

    ---

    Special Method Usage
    --------------------

    Objects have been designed to be almost interchangable with \
    dictionaries. The primary difference is that values cannot be \
    assigned to keys unless you define them on the Object's class \
    definition itself.
    * This is done to automatically maximize the efficiency of your \
    application's memory footprint. Feel free to read more about \
    python [slots](https://wiki.python.org/moin/UsingSlots) to better \
    understand why this is necessary.

    ```py
    import fgr


    class Pet(fgr.Object):  # noqa

        name: fgr.Field[str]


    dog = Pet(name='Fido')

    # The below would return the string, 'Fido'.
    dog['name']

    # The following would set the dog's name to something else.
    dog.setdefault('name', 'Arnold')
    assert dog.name == 'Arnold'
    dog.setdefault('name', 'Buddy')
    assert dog.name == 'Arnold'
    dog['name'] = 'Buddy'
    assert dog.name == 'Buddy'
    assert dog['name'] == 'Buddy'

    # The following all work exactly the same as with a dictionary.
    # (in the below, key will be 'name' and value 'Fido').
    for key, value in dog.items():
        break

    for key in dog.keys():
        break

    for value in dog.values():
        break

    # But the following will raise a KeyError.
    dog['field_that_does_not_exist'] = 'Buddy'

    # And so would this, since fields can only be added
    # or removed on the class definition of Pet itself.
    dog.setdefault('field_that_does_not_exist', 'Buddy')

    ```

    Object truthiness will evaluate to True if any values for \
    the Object instance are different from default values, \
    otherwise False.

    ```py
    if Object:
    ```

    Objects are designed to display themselves as neatly \
    formatted JSON on calls to `__repr__`.

    ```py
    print(Object)
    ```

    Updates Object1 with values from Object2 if they \
    are a non-default value for the object.

    ```py
    Object1 << Object2
    ```

    Overwrites Object1 values with those from Object2 \
    if they are a non-default value for the object.

    ```py
    Object1 >> Object2
    ```

    Returns a dictionary with {fieldName: fieldValue2} for \
    any fields that differ between the two Objects.

    ```py
    Object1 - Object2
    ```

    Get value for Object field.

    ```py
    value = Object['field']
    ```

    Set value for Object field.

    ```py
    Object['field'] = value
    ```

    Returns True if any one of field, _field, field_, or _field_ \
    is a valid field for the Object, otherwise False.

    ```py
    field in Object
    ```

    Same as `len(Object.fields)`.

    ```py
    len(Object)
    ```

    Querying Databases
    ------------------


    Queries for `Objects` can be generated from their fields \
    using the following comparison operators:

    * `field_1_eq_filter = Object.field_1 == 'test_value_123'`
    * `field_1_ne_filter = Object.field_1 != 'test_value_123'`
    * `field_1_ge_filter = Object.field_1 >= 'test_value_123'`
    * `field_1_gt_filter = Object.field_1 > 'test_value_123'`
    * `field_1_le_filter = Object.field_1 <= 'test_value_123'`
    * `field_1_lt_filter = Object.field_1 < 'test_value_123'`

    And the following special operators:

    * `field_1_contains_filter = Object.field_1 << 'test_value_123'`
    * `field_1_similarity_filter = Object.field_1 % 'test_value_123'`
    * `field_1_similarity_filter_with_threshold = Object.field_1 % ('test_value_123', 0.8)`

    Queries may be chained together using the `&` and `|` bitwise \
    operators, corresponding to `and` and `or` clauses respectively.

    Additionally, the invert (`~`) operator may be prefixed to any \
    Query to match the opposite of any conditions specified \
    instead.

    """
