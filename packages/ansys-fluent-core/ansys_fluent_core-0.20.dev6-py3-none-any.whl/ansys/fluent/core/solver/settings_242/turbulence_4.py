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

from .les_spec_name import les_spec_name as les_spec_name_cls
from .rfg_number_of_modes import rfg_number_of_modes as rfg_number_of_modes_cls
from .vm_nvortices import vm_nvortices as vm_nvortices_cls
from .les_embedded_fluctuations import les_embedded_fluctuations as les_embedded_fluctuations_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['les_spec_name', 'rfg_number_of_modes', 'vm_nvortices',
         'les_embedded_fluctuations']

    _child_classes = dict(
        les_spec_name=les_spec_name_cls,
        rfg_number_of_modes=rfg_number_of_modes_cls,
        vm_nvortices=vm_nvortices_cls,
        les_embedded_fluctuations=les_embedded_fluctuations_cls,
    )

