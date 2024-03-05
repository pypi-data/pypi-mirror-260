import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_point(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    location: typing.Optional[typing.Any] = (0, 0),
):
    """Add New Paint Curve Point

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param location: Location, Location of vertex in area space
    :type location: typing.Optional[typing.Any]
    """

    ...

def add_point_slide(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    PAINTCURVE_OT_add_point: typing.Optional["add_point"] = None,
    PAINTCURVE_OT_slide: typing.Optional["slide"] = None,
):
    """Add new curve point and slide it

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param PAINTCURVE_OT_add_point: Add New Paint Curve Point, Add New Paint Curve Point
    :type PAINTCURVE_OT_add_point: typing.Optional['add_point']
    :param PAINTCURVE_OT_slide: Slide Paint Curve Point, Select and slide paint curve point
    :type PAINTCURVE_OT_slide: typing.Optional['slide']
    """

    ...

def cursor(override_context=None, execution_context=None, undo=None):
    """Place cursor

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete_point(override_context=None, execution_context=None, undo=None):
    """Remove Paint Curve Point

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def draw(override_context=None, execution_context=None, undo=None):
    """Draw curve

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def new(override_context=None, execution_context=None, undo=None):
    """Add new paint curve

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def select(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    location: typing.Optional[typing.Any] = (0, 0),
    toggle: typing.Optional[typing.Union[bool, typing.Any]] = False,
    extend: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select a paint curve point

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param location: Location, Location of vertex in area space
    :type location: typing.Optional[typing.Any]
    :param toggle: Toggle, (De)select all
    :type toggle: typing.Optional[typing.Union[bool, typing.Any]]
    :param extend: Extend, Extend selection
    :type extend: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def slide(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    align: typing.Optional[typing.Union[bool, typing.Any]] = False,
    select: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Select and slide paint curve point

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param align: Align Handles, Aligns opposite point handle during transform
    :type align: typing.Optional[typing.Union[bool, typing.Any]]
    :param select: Select, Attempt to select a point handle before transform
    :type select: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
