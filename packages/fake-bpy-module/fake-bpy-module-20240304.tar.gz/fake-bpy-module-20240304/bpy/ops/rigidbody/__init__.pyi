import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def bake_to_keyframes(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    frame_start: typing.Optional[typing.Any] = 1,
    frame_end: typing.Optional[typing.Any] = 250,
    step: typing.Optional[typing.Any] = 1,
):
    """Bake rigid body transformations of selected objects to keyframes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param frame_start: Start Frame, Start frame for baking
    :type frame_start: typing.Optional[typing.Any]
    :param frame_end: End Frame, End frame for baking
    :type frame_end: typing.Optional[typing.Any]
    :param step: Frame Step, Frame Step
    :type step: typing.Optional[typing.Any]
    """

    ...

def connect(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    con_type: typing.Optional[typing.Any] = "FIXED",
    pivot_type: typing.Optional[typing.Any] = "CENTER",
    connection_pattern: typing.Optional[typing.Any] = "SELECTED_TO_ACTIVE",
):
    """Create rigid body constraints between selected rigid bodies

        :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
        :type execution_context: typing.Optional[typing.Union[int, str]]
        :type undo: typing.Optional[bool]
        :param con_type: Type, Type of generated constraint

    FIXED
    Fixed -- Glue rigid bodies together.

    POINT
    Point -- Constrain rigid bodies to move around common pivot point.

    HINGE
    Hinge -- Restrict rigid body rotation to one axis.

    SLIDER
    Slider -- Restrict rigid body translation to one axis.

    PISTON
    Piston -- Restrict rigid body translation and rotation to one axis.

    GENERIC
    Generic -- Restrict translation and rotation to specified axes.

    GENERIC_SPRING
    Generic Spring -- Restrict translation and rotation to specified axes with springs.

    MOTOR
    Motor -- Drive rigid body around or along an axis.
        :type con_type: typing.Optional[typing.Any]
        :param pivot_type: Location, Constraint pivot location

    CENTER
    Center -- Pivot location is between the constrained rigid bodies.

    ACTIVE
    Active -- Pivot location is at the active object position.

    SELECTED
    Selected -- Pivot location is at the selected object position.
        :type pivot_type: typing.Optional[typing.Any]
        :param connection_pattern: Connection Pattern, Pattern used to connect objects

    SELECTED_TO_ACTIVE
    Selected to Active -- Connect selected objects to the active object.

    CHAIN_DISTANCE
    Chain by Distance -- Connect objects as a chain based on distance, starting at the active object.
        :type connection_pattern: typing.Optional[typing.Any]
    """

    ...

def constraint_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "FIXED",
):
    """Add Rigid Body Constraint to active object

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Rigid Body Constraint Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def constraint_remove(override_context=None, execution_context=None, undo=None):
    """Remove Rigid Body Constraint from Object

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def mass_calculate(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    material: typing.Optional[typing.Union[int, str, typing.Any]] = "DEFAULT",
    density: typing.Optional[typing.Any] = 1.0,
):
    """Automatically calculate mass values for Rigid Body Objects based on volume

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param material: Material Preset, Type of material that objects are made of (determines material density)
    :type material: typing.Optional[typing.Union[int, str, typing.Any]]
    :param density: Density, Density value (kg/m^3), allows custom value if the 'Custom' preset is used
    :type density: typing.Optional[typing.Any]
    """

    ...

def object_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "ACTIVE",
):
    """Add active object as Rigid Body

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Rigid Body Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def object_remove(override_context=None, execution_context=None, undo=None):
    """Remove Rigid Body settings from Object

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def object_settings_copy(override_context=None, execution_context=None, undo=None):
    """Copy Rigid Body settings from active object to selected

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def objects_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "ACTIVE",
):
    """Add selected objects as Rigid Bodies

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Rigid Body Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def objects_remove(override_context=None, execution_context=None, undo=None):
    """Remove selected objects from Rigid Body simulation

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def shape_change(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "MESH",
):
    """Change collision shapes for selected Rigid Body Objects

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Rigid Body Shape
    :type type: typing.Optional[typing.Any]
    """

    ...

def world_add(override_context=None, execution_context=None, undo=None):
    """Add Rigid Body simulation world to the current scene

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def world_remove(override_context=None, execution_context=None, undo=None):
    """Remove Rigid Body simulation world from the current scene

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
