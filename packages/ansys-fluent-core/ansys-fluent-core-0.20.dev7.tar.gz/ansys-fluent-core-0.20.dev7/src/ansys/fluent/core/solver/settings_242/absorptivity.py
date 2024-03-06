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

from .v_opq_absorbtivity import v_opq_absorbtivity as v_opq_absorbtivity_cls
from .v_st_absorbtivity import v_st_absorbtivity as v_st_absorbtivity_cls
from .ir_opq_absorbtivity import ir_opq_absorbtivity as ir_opq_absorbtivity_cls
from .ir_st_absorbtivity import ir_st_absorbtivity as ir_st_absorbtivity_cls
from .d_st_absorbtivity import d_st_absorbtivity as d_st_absorbtivity_cls
class absorptivity(Group):
    """
    Absorptivity settings.
    """

    fluent_name = "absorptivity"

    child_names = \
        ['v_opq_absorbtivity', 'v_st_absorbtivity', 'ir_opq_absorbtivity',
         'ir_st_absorbtivity', 'd_st_absorbtivity']

    _child_classes = dict(
        v_opq_absorbtivity=v_opq_absorbtivity_cls,
        v_st_absorbtivity=v_st_absorbtivity_cls,
        ir_opq_absorbtivity=ir_opq_absorbtivity_cls,
        ir_st_absorbtivity=ir_st_absorbtivity_cls,
        d_st_absorbtivity=d_st_absorbtivity_cls,
    )

