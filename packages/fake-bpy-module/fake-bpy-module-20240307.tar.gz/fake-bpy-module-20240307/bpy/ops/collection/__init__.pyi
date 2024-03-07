import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def create(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "Collection",
):
    """Create an object collection from selected objects

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the new collection
    :type name: typing.Union[str, typing.Any]
    """

    ...

def objects_add_active(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    collection: typing.Optional[typing.Union[int, str, typing.Any]] = "",
):
    """Add the object to an object collection that contains the active object

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param collection: Collection, The collection to add other selected objects to
    :type collection: typing.Optional[typing.Union[int, str, typing.Any]]
    """

    ...

def objects_remove(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    collection: typing.Optional[typing.Union[int, str, typing.Any]] = "",
):
    """Remove selected objects from a collection

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param collection: Collection, The collection to remove this object from
    :type collection: typing.Optional[typing.Union[int, str, typing.Any]]
    """

    ...

def objects_remove_active(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    collection: typing.Optional[typing.Union[int, str, typing.Any]] = "",
):
    """Remove the object from an object collection that contains the active object

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param collection: Collection, The collection to remove other selected objects from
    :type collection: typing.Optional[typing.Union[int, str, typing.Any]]
    """

    ...

def objects_remove_all(override_context=None, execution_context=None, undo=None):
    """Remove selected objects from all collections

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
