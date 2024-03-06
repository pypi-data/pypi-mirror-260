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

from .enabled_23 import enabled as enabled_cls
from .venting_gas_phase import venting_gas_phase as venting_gas_phase_cls
from .gas_release_faces import gas_release_faces as gas_release_faces_cls
from .reacting_model import reacting_model as reacting_model_cls
from .rate_method import rate_method as rate_method_cls
from .one_mass import one_mass as one_mass_cls
from .four_sei import four_sei as four_sei_cls
from .four_pe import four_pe as four_pe_cls
from .four_ne import four_ne as four_ne_cls
from .four_e import four_e as four_e_cls
from .trigger_t_1 import trigger_t as trigger_t_cls
from .rate_file import rate_file as rate_file_cls
from .gas_composition import gas_composition as gas_composition_cls
class venting_model(Group):
    """
    Venting model settings.
    """

    fluent_name = "venting-model"

    child_names = \
        ['enabled', 'venting_gas_phase', 'gas_release_faces',
         'reacting_model', 'rate_method', 'one_mass', 'four_sei', 'four_pe',
         'four_ne', 'four_e', 'trigger_t', 'rate_file', 'gas_composition']

    _child_classes = dict(
        enabled=enabled_cls,
        venting_gas_phase=venting_gas_phase_cls,
        gas_release_faces=gas_release_faces_cls,
        reacting_model=reacting_model_cls,
        rate_method=rate_method_cls,
        one_mass=one_mass_cls,
        four_sei=four_sei_cls,
        four_pe=four_pe_cls,
        four_ne=four_ne_cls,
        four_e=four_e_cls,
        trigger_t=trigger_t_cls,
        rate_file=rate_file_cls,
        gas_composition=gas_composition_cls,
    )

