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

from .enable_6 import enable as enable_cls
from .solution_method import solution_method as solution_method_cls
class do_energy_coupling(Group):
    """
    Settings for DO/Energy Coupling.
    """

    fluent_name = "do-energy-coupling"

    child_names = \
        ['enable', 'solution_method']

    _child_classes = dict(
        enable=enable_cls,
        solution_method=solution_method_cls,
    )

