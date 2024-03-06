import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def new(override_context=None, execution_context=None, undo=None):
    """Create a new world Data-Block

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
