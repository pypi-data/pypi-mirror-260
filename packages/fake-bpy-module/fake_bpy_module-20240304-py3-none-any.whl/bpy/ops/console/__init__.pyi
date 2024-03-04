import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def autocomplete(override_context=None, execution_context=None, undo=None):
    """Evaluate the namespace up until the cursor and give a list of options or complete the name if there is only one

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def banner(override_context=None, execution_context=None, undo=None):
    """Print a message when the terminal initializes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def clear(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    scrollback: typing.Optional[typing.Union[bool, typing.Any]] = True,
    history: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Clear text by type

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param scrollback: Scrollback, Clear the scrollback history
    :type scrollback: typing.Optional[typing.Union[bool, typing.Any]]
    :param history: History, Clear the command history
    :type history: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def clear_line(override_context=None, execution_context=None, undo=None):
    """Clear the line and store in history

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def copy(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    delete: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Copy selected text to clipboard

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param delete: Delete Selection, Whether to delete the selection after copying
    :type delete: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def copy_as_script(override_context=None, execution_context=None, undo=None):
    """Copy the console contents for use in a script

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "NEXT_CHARACTER",
):
    """Delete text by cursor position

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type, Which part of the text to delete
    :type type: typing.Optional[typing.Any]
    """

    ...

def execute(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    interactive: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Execute the current console line as a Python expression

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param interactive: interactive
    :type interactive: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def history_append(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    text: typing.Union[str, typing.Any] = "",
    current_character: typing.Optional[typing.Any] = 0,
    remove_duplicates: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Append history at cursor position

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param text: Text, Text to insert at the cursor position
    :type text: typing.Union[str, typing.Any]
    :param current_character: Cursor, The index of the cursor
    :type current_character: typing.Optional[typing.Any]
    :param remove_duplicates: Remove Duplicates, Remove duplicate items in the history
    :type remove_duplicates: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def history_cycle(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    reverse: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Cycle through history

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param reverse: Reverse, Reverse cycle history
    :type reverse: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def indent(override_context=None, execution_context=None, undo=None):
    """Add 4 spaces at line beginning

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def indent_or_autocomplete(override_context=None, execution_context=None, undo=None):
    """Indent selected text or autocomplete

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def insert(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    text: typing.Union[str, typing.Any] = "",
):
    """Insert text at cursor position

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param text: Text, Text to insert at the cursor position
    :type text: typing.Union[str, typing.Any]
    """

    ...

def language(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    language: typing.Union[str, typing.Any] = "",
):
    """Set the current language for this console

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param language: Language
    :type language: typing.Union[str, typing.Any]
    """

    ...

def move(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "LINE_BEGIN",
    select: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Move cursor position

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type, Where to move cursor to
    :type type: typing.Optional[typing.Any]
    :param select: Select, Whether to select while moving
    :type select: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def paste(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    selection: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Paste text from clipboard

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param selection: Selection, Paste text selected elsewhere rather than copied (X11/Wayland only)
    :type selection: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def scrollback_append(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    text: typing.Union[str, typing.Any] = "",
    type: typing.Optional[typing.Any] = "OUTPUT",
):
    """Append scrollback text by type

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param text: Text, Text to insert at the cursor position
    :type text: typing.Union[str, typing.Any]
    :param type: Type, Console output type
    :type type: typing.Optional[typing.Any]
    """

    ...

def select_all(override_context=None, execution_context=None, undo=None):
    """Select all the text

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_set(override_context=None, execution_context=None, undo=None):
    """Set the console selection

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_word(override_context=None, execution_context=None, undo=None):
    """Select word at cursor position

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def unindent(override_context=None, execution_context=None, undo=None):
    """Delete 4 spaces from line beginning

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
