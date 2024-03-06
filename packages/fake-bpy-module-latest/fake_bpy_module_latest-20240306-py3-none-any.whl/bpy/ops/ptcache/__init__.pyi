import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add(override_context=None, execution_context=None, undo=None):
    """Add new cache

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def bake(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    bake: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Bake physics

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param bake: Bake
    :type bake: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def bake_all(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    bake: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Bake all physics

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param bake: Bake
    :type bake: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def bake_from_cache(override_context=None, execution_context=None, undo=None):
    """Bake from cache

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def free_bake(override_context=None, execution_context=None, undo=None):
    """Delete physics bake

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def free_bake_all(override_context=None, execution_context=None, undo=None):
    """Delete all baked caches of all objects in the current scene

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def remove(override_context=None, execution_context=None, undo=None):
    """Delete current cache

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
