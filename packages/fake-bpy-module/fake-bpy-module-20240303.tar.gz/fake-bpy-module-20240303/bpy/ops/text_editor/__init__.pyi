import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add or remove a Text Editor Preset

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the preset, used to make the path name
    :type name: typing.Union[str, typing.Any]
    :param remove_name: remove_name
    :type remove_name: typing.Optional[typing.Union[bool, typing.Any]]
    :param remove_active: remove_active
    :type remove_active: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
