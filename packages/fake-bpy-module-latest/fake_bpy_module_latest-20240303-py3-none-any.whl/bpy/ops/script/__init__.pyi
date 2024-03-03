import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def execute_preset(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    filepath: typing.Union[str, typing.Any] = "",
    menu_idname: typing.Union[str, typing.Any] = "",
):
    """Load a preset

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param menu_idname: Menu ID Name, ID name of the menu this was called from
    :type menu_idname: typing.Union[str, typing.Any]
    """

    ...

def python_file_run(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    filepath: typing.Union[str, typing.Any] = "",
):
    """Run Python file

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param filepath: Path
    :type filepath: typing.Union[str, typing.Any]
    """

    ...

def reload(override_context=None, execution_context=None, undo=None):
    """Reload scripts

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
