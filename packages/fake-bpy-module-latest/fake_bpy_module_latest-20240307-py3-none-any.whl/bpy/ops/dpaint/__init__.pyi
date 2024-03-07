import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def bake(override_context=None, execution_context=None, undo=None):
    """Bake dynamic paint image sequence surface

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def output_toggle(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    output: typing.Optional[typing.Any] = "A",
):
    """Add or remove Dynamic Paint output data layer

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param output: Output Toggle
    :type output: typing.Optional[typing.Any]
    """

    ...

def surface_slot_add(override_context=None, execution_context=None, undo=None):
    """Add a new Dynamic Paint surface slot

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def surface_slot_remove(override_context=None, execution_context=None, undo=None):
    """Remove the selected surface slot

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def type_toggle(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "CANVAS",
):
    """Toggle whether given type is active or not

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...
