import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def svg(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    filepath: typing.Union[str, typing.Any] = "",
    filter_glob: typing.Union[str, typing.Any] = "*.svg",
):
    """Load a SVG file

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param filepath: File Path, Filepath used for importing the file
    :type filepath: typing.Union[str, typing.Any]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    """

    ...
