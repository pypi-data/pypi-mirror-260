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

from .molef_ref_h2 import molef_ref_h2 as molef_ref_h2_cls
from .molef_ref_o2 import molef_ref_o2 as molef_ref_o2_cls
from .molef_ref_h2o import molef_ref_h2o as molef_ref_h2o_cls
class mole_fraction_ref(Group):
    """
    Enter the mole fraction reference settings.
    """

    fluent_name = "mole-fraction-ref"

    child_names = \
        ['molef_ref_h2', 'molef_ref_o2', 'molef_ref_h2o']

    _child_classes = dict(
        molef_ref_h2=molef_ref_h2_cls,
        molef_ref_o2=molef_ref_o2_cls,
        molef_ref_h2o=molef_ref_h2o_cls,
    )

