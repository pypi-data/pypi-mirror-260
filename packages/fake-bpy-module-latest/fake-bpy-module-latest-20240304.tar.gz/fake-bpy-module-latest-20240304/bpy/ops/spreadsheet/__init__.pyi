import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_row_filter_rule(override_context=None, execution_context=None, undo=None):
    """Add a filter to remove rows from the displayed data

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def change_spreadsheet_data_source(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    component_type: typing.Optional[typing.Any] = 0,
    attribute_domain_type: typing.Optional[typing.Any] = 0,
):
    """Change visible data source in the spreadsheet

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param component_type: Component Type
    :type component_type: typing.Optional[typing.Any]
    :param attribute_domain_type: Attribute Domain Type
    :type attribute_domain_type: typing.Optional[typing.Any]
    """

    ...

def remove_row_filter_rule(
    override_context=None,
    execution_context=None,
    undo=None,
    *,
    index: typing.Optional[typing.Any] = 0,
):
    """Remove a row filter from the rules

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param index: Index
    :type index: typing.Optional[typing.Any]
    """

    ...

def toggle_pin(override_context=None, execution_context=None, undo=None):
    """Turn on or off pinning

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
