import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def rule_add(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    type: typing.Optional[typing.Any] = "GOAL",
):
    """Add a boid rule to the current boid state

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def rule_del(override_context=None, execution_context=None, undo=None):
    """Delete current boid rule

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def rule_move_down(override_context=None, execution_context=None, undo=None):
    """Move boid rule down in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def rule_move_up(override_context=None, execution_context=None, undo=None):
    """Move boid rule up in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def state_add(override_context=None, execution_context=None, undo=None):
    """Add a boid state to the particle system

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def state_del(override_context=None, execution_context=None, undo=None):
    """Delete current boid state

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def state_move_down(override_context=None, execution_context=None, undo=None):
    """Move boid state down in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def state_move_up(override_context=None, execution_context=None, undo=None):
    """Move boid state up in the list

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
