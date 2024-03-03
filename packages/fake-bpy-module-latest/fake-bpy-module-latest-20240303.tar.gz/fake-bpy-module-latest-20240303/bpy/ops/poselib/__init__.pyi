import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def apply_pose_asset(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    blend_factor: typing.Optional[typing.Any] = 1.0,
    flipped: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Apply the given Pose Action to the rig

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: typing.Optional[typing.Any]
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def blend_pose_asset(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    blend_factor: typing.Optional[typing.Any] = 0.0,
    flipped: typing.Optional[typing.Union[bool, typing.Any]] = False,
    release_confirm: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Blend the given Pose Action to the rig

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: typing.Optional[typing.Any]
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: typing.Optional[typing.Union[bool, typing.Any]]
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button
    :type release_confirm: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def convert_old_object_poselib(
    override_context=None, execution_context=None, undo=None
):
    """Create a pose asset for each pose marker in this legacy pose library data-block

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def convert_old_poselib(override_context=None, execution_context=None, undo=None):
    """Create a pose asset for each pose marker in the current action

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def copy_as_asset(override_context=None, execution_context=None, undo=None):
    """Create a new pose asset on the clipboard, to be pasted into an Asset Browser

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def create_pose_asset(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    pose_name: typing.Union[str, typing.Any] = "",
    activate_new_action: typing.Optional[typing.Union[bool, typing.Any]] = True,
):
    """Create a new Action that contains the pose of the selected bones, and mark it as Asset. The asset will be stored in the current blend file

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param pose_name: Pose Name
    :type pose_name: typing.Union[str, typing.Any]
    :param activate_new_action: Activate New Action
    :type activate_new_action: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def paste_asset(override_context=None, execution_context=None, undo=None):
    """Paste the Asset that was previously copied using Copy As Asset

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def pose_asset_select_bones(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    select: typing.Optional[typing.Union[bool, typing.Any]] = True,
    flipped: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Select those bones that are used in this pose

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param select: Select
    :type select: typing.Optional[typing.Union[bool, typing.Any]]
    :param flipped: Flipped
    :type flipped: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def restore_previous_action(override_context=None, execution_context=None, undo=None):
    """Switch back to the previous Action, after creating a pose asset

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
