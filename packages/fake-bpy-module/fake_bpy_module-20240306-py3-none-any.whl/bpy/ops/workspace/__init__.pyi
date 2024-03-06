import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add(override_context=None, execution_context=None, undo=None):
    """Add a new workspace by duplicating the current one or appending one from the user configuration

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def append_activate(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    idname: typing.Union[str, typing.Any] = "",
    filepath: typing.Union[str, typing.Any] = "",
):
    """Append a workspace and make it the active one in the current window

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param idname: Identifier, Name of the workspace to append and activate
    :type idname: typing.Union[str, typing.Any]
    :param filepath: Filepath, Path to the library
    :type filepath: typing.Union[str, typing.Any]
    """

    ...

def delete(override_context=None, execution_context=None, undo=None):
    """Delete the active workspace

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def duplicate(override_context=None, execution_context=None, undo=None):
    """Add a new workspace

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def reorder_to_back(override_context=None, execution_context=None, undo=None):
    """Reorder workspace to be last in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def reorder_to_front(override_context=None, execution_context=None, undo=None):
    """Reorder workspace to be first in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def scene_pin_toggle(override_context=None, execution_context=None, undo=None):
    """Remember the last used scene for the current workspace and switch to it whenever this workspace is activated again

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
