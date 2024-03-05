import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def copy(override_context=None, execution_context=None, undo=None):
    """Copy the material settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def new(override_context=None, execution_context=None, undo=None):
    """Add a new material

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def paste(override_context=None, execution_context=None, undo=None):
    """Paste the material settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
