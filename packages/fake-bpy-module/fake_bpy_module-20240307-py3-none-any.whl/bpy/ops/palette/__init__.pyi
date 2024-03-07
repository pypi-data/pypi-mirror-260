import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def color_add(override_context=None, execution_context=None, undo=None):
    """Add new color to active palette

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def color_delete(override_context=None, execution_context=None, undo=None):
    """Remove active color from palette

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def color_move(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "UP",
):
    """Move the active Color up/down in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def extract_from_image(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    threshold: typing.Optional[typing.Any] = 1,
):
    """Extract all colors used in Image and create a Palette

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param threshold: Threshold
    :type threshold: typing.Optional[typing.Any]
    """

    ...

def join(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    palette: typing.Union[str, typing.Any] = "",
):
    """Join Palette Swatches

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param palette: Palette, Name of the Palette
    :type palette: typing.Union[str, typing.Any]
    """

    ...

def new(override_context=None, execution_context=None, undo=None):
    """Add new palette

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def sort(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "HSV",
):
    """Sort Palette Colors

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...
