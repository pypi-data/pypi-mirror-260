import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def report_copy(override_context=None, execution_context=None, undo=None):
    """Copy selected reports to clipboard

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def report_delete(override_context=None, execution_context=None, undo=None):
    """Delete selected reports

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def report_replay(override_context=None, execution_context=None, undo=None):
    """Replay selected reports

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def reports_display_update(override_context=None, execution_context=None, undo=None):
    """Update the display of reports in Blender UI (internal use)

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_all(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    action: typing.Optional[typing.Any] = "SELECT",
):
    """Change selection of all visible reports

        :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
        :type execution_context: typing.Optional[typing.Union[int, str]]
        :type undo: typing.Optional[bool]
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Optional[typing.Any]
    """

    ...

def select_box(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    xmin: typing.Optional[typing.Any] = 0,
    xmax: typing.Optional[typing.Any] = 0,
    ymin: typing.Optional[typing.Any] = 0,
    ymax: typing.Optional[typing.Any] = 0,
    wait_for_input: typing.Optional[typing.Union[bool, typing.Any]] = True,
    mode: typing.Optional[typing.Any] = "SET",
):
    """Toggle box selection

        :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
        :type execution_context: typing.Optional[typing.Union[int, str]]
        :type undo: typing.Optional[bool]
        :param xmin: X Min
        :type xmin: typing.Optional[typing.Any]
        :param xmax: X Max
        :type xmax: typing.Optional[typing.Any]
        :param ymin: Y Min
        :type ymin: typing.Optional[typing.Any]
        :param ymax: Y Max
        :type ymax: typing.Optional[typing.Any]
        :param wait_for_input: Wait for Input
        :type wait_for_input: typing.Optional[typing.Union[bool, typing.Any]]
        :param mode: Mode

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :type mode: typing.Optional[typing.Any]
    """

    ...

def select_pick(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    report_index: typing.Optional[typing.Any] = 0,
    extend: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select reports by index

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param report_index: Report, Index of the report
    :type report_index: typing.Optional[typing.Any]
    :param extend: Extend, Extend report selection
    :type extend: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
