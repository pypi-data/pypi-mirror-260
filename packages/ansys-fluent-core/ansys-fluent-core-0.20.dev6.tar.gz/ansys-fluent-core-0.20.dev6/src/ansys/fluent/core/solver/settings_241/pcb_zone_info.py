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

from .ecad_name import ecad_name as ecad_name_cls
from .choice import choice as choice_cls
from .rows import rows as rows_cls
from .columns import columns as columns_cls
from .ref_frame import ref_frame as ref_frame_cls
from .pwr_names import pwr_names as pwr_names_cls
class pcb_zone_info(Group):
    """
    'pcb_zone_info' child.
    """

    fluent_name = "pcb-zone-info"

    child_names = \
        ['ecad_name', 'choice', 'rows', 'columns', 'ref_frame', 'pwr_names']

    _child_classes = dict(
        ecad_name=ecad_name_cls,
        choice=choice_cls,
        rows=rows_cls,
        columns=columns_cls,
        ref_frame=ref_frame_cls,
        pwr_names=pwr_names_cls,
    )

