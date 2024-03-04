import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def entry_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    list_path: typing.Union[str, typing.Any] = "",
    active_index_path: typing.Union[str, typing.Any] = "",
):
    """Add an entry to the list after the current active item

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param list_path: list_path
    :type list_path: typing.Union[str, typing.Any]
    :param active_index_path: active_index_path
    :type active_index_path: typing.Union[str, typing.Any]
    """

    ...

def entry_move(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    list_path: typing.Union[str, typing.Any] = "",
    active_index_path: typing.Union[str, typing.Any] = "",
    direction: typing.Optional[typing.Any] = "UP",
):
    """Move an entry in the list up or down

        :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
        :type execution_context: typing.Optional[typing.Union[int, str]]
        :type undo: typing.Optional[bool]
        :param list_path: list_path
        :type list_path: typing.Union[str, typing.Any]
        :param active_index_path: active_index_path
        :type active_index_path: typing.Union[str, typing.Any]
        :param direction: Direction

    UP
    UP -- UP.

    DOWN
    DOWN -- DOWN.
        :type direction: typing.Optional[typing.Any]
    """

    ...

def entry_remove(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    list_path: typing.Union[str, typing.Any] = "",
    active_index_path: typing.Union[str, typing.Any] = "",
):
    """Remove the selected entry from the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param list_path: list_path
    :type list_path: typing.Union[str, typing.Any]
    :param active_index_path: active_index_path
    :type active_index_path: typing.Union[str, typing.Any]
    """

    ...
