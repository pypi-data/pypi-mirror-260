import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def attribute_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    domain: typing.Optional[typing.Any] = "POINT",
    data_type: typing.Optional[typing.Any] = "FLOAT",
):
    """Add attribute to geometry

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of new attribute
    :type name: typing.Union[str, typing.Any]
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: typing.Optional[typing.Any]
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: typing.Optional[typing.Any]
    """

    ...

def attribute_convert(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    mode: typing.Optional[typing.Any] = "GENERIC",
    domain: typing.Optional[typing.Any] = "POINT",
    data_type: typing.Optional[typing.Any] = "FLOAT",
):
    """Change how the attribute is stored

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param mode: Mode
    :type mode: typing.Optional[typing.Any]
    :param domain: Domain, Which geometry element to move the attribute to
    :type domain: typing.Optional[typing.Any]
    :param data_type: Data Type
    :type data_type: typing.Optional[typing.Any]
    """

    ...

def attribute_remove(override_context=None, execution_context=None, undo=None):
    """Remove attribute from geometry

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def color_attribute_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    domain: typing.Optional[typing.Any] = "POINT",
    data_type: typing.Optional[typing.Any] = "FLOAT_COLOR",
    color: typing.Optional[typing.Any] = (0.0, 0.0, 0.0, 1.0),
):
    """Add color attribute to geometry

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of new color attribute
    :type name: typing.Union[str, typing.Any]
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: typing.Optional[typing.Any]
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: typing.Optional[typing.Any]
    :param color: Color, Default fill color
    :type color: typing.Optional[typing.Any]
    """

    ...

def color_attribute_convert(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    domain: typing.Optional[typing.Any] = "POINT",
    data_type: typing.Optional[typing.Any] = "FLOAT_COLOR",
):
    """Change how the color attribute is stored

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: typing.Optional[typing.Any]
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: typing.Optional[typing.Any]
    """

    ...

def color_attribute_duplicate(override_context=None, execution_context=None, undo=None):
    """Duplicate color attribute

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def color_attribute_remove(override_context=None, execution_context=None, undo=None):
    """Remove color attribute from geometry

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def color_attribute_render_set(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "Color",
):
    """Set default color attribute used for rendering

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of color attribute
    :type name: typing.Union[str, typing.Any]
    """

    ...

def execute_node_group(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    asset_library_type: typing.Optional[typing.Any] = "LOCAL",
    asset_library_identifier: typing.Union[str, typing.Any] = "",
    relative_asset_identifier: typing.Union[str, typing.Any] = "",
    name: typing.Union[str, typing.Any] = "",
    session_uid: typing.Optional[typing.Any] = 0,
):
    """Execute a node group on geometry

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param asset_library_type: Asset Library Type
    :type asset_library_type: typing.Optional[typing.Any]
    :param asset_library_identifier: Asset Library Identifier
    :type asset_library_identifier: typing.Union[str, typing.Any]
    :param relative_asset_identifier: Relative Asset Identifier
    :type relative_asset_identifier: typing.Union[str, typing.Any]
    :param name: Name, Name of the data-block to use by the operator
    :type name: typing.Union[str, typing.Any]
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Optional[typing.Any]
    """

    ...

def geometry_randomization(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    value: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Toggle geometry randomization for debugging purposes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param value: Value, Randomize the order of geometry elements (e.g. vertices or edges) after some operations where there are no guarantees about the order. This avoids accidentally depending on something that may change in the future
    :type value: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
