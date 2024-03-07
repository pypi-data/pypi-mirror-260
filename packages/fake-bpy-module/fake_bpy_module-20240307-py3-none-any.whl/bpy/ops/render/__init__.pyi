import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def cycles_integrator_preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add an Integrator Preset

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

def cycles_performance_preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add an Performance Preset

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

def cycles_sampling_preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add a Sampling Preset

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

def cycles_viewport_sampling_preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add a Viewport Sampling Preset

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

def eevee_raytracing_preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add or remove an EEVEE ray-tracing preset

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

def opengl(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    animation: typing.Optional[typing.Union[bool, typing.Any]] = False,
    render_keyed_only: typing.Optional[typing.Union[bool, typing.Any]] = False,
    sequencer: typing.Optional[typing.Union[bool, typing.Any]] = False,
    write_still: typing.Optional[typing.Union[bool, typing.Any]] = False,
    view_context: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Take a snapshot of the active viewport

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param animation: Animation, Render files from the animation range of this scene
    :type animation: typing.Optional[typing.Union[bool, typing.Any]]
    :param render_keyed_only: Render Keyframes Only, Render only those frames where selected objects have a key in their animation data. Only used when rendering animation
    :type render_keyed_only: typing.Optional[typing.Union[bool, typing.Any]]
    :param sequencer: Sequencer, Render using the sequencer's OpenGL display
    :type sequencer: typing.Optional[typing.Union[bool, typing.Any]]
    :param write_still: Write Image, Save the rendered image to the output path (used only when animation is disabled)
    :type write_still: typing.Optional[typing.Union[bool, typing.Any]]
    :param view_context: View Context, Use the current 3D view for rendering, else use scene settings
    :type view_context: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def play_rendered_anim(override_context=None, execution_context=None, undo=None):
    """Play back rendered frames/movies using an external player

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def preset_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add or remove a Render Preset

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

def render(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    animation: typing.Optional[typing.Union[bool, typing.Any]] = False,
    write_still: typing.Optional[typing.Union[bool, typing.Any]] = False,
    use_viewport: typing.Optional[typing.Union[bool, typing.Any]] = False,
    layer: typing.Union[str, typing.Any] = "",
    scene: typing.Union[str, typing.Any] = "",
):
    """Render active scene

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param animation: Animation, Render files from the animation range of this scene
    :type animation: typing.Optional[typing.Union[bool, typing.Any]]
    :param write_still: Write Image, Save the rendered image to the output path (used only when animation is disabled)
    :type write_still: typing.Optional[typing.Union[bool, typing.Any]]
    :param use_viewport: Use 3D Viewport, When inside a 3D viewport, use layers and camera of the viewport
    :type use_viewport: typing.Optional[typing.Union[bool, typing.Any]]
    :param layer: Render Layer, Single render layer to re-render (used only when animation is disabled)
    :type layer: typing.Union[str, typing.Any]
    :param scene: Scene, Scene to render, current scene if not specified
    :type scene: typing.Union[str, typing.Any]
    """

    ...

def shutter_curve_preset(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    shape: typing.Optional[typing.Any] = "SMOOTH",
):
    """Set shutter curve

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param shape: Mode
    :type shape: typing.Optional[typing.Any]
    """

    ...

def view_cancel(override_context=None, execution_context=None, undo=None):
    """Cancel show render view

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def view_show(override_context=None, execution_context=None, undo=None):
    """Toggle show render view

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
