#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .cathode_fc_zone_list import cathode_fc_zone_list as cathode_fc_zone_list_cls
class cathode_fc_zone(Group):
    """
    Set up cathode flow channel.
    """

    fluent_name = "cathode-fc-zone"

    child_names = \
        ['cathode_fc_zone_list']

    _child_classes = dict(
        cathode_fc_zone_list=cathode_fc_zone_list_cls,
    )

