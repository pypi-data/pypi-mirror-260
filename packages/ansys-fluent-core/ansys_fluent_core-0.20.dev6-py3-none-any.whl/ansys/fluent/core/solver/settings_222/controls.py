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

from .acoustics_wave_equation_controls import acoustics_wave_equation_controls as acoustics_wave_equation_controls_cls
from .advanced import advanced as advanced_cls
from .contact_solution_controls import contact_solution_controls as contact_solution_controls_cls
from .courant_number import courant_number as courant_number_cls
from .equations import equations as equations_cls
from .limits import limits as limits_cls
from .p_v_controls import p_v_controls as p_v_controls_cls
from .relaxation_factor_1 import relaxation_factor as relaxation_factor_cls
from .set_controls_to_default import set_controls_to_default as set_controls_to_default_cls
from .under_relaxation import under_relaxation as under_relaxation_cls
class controls(Group):
    """
    'controls' child.
    """

    fluent_name = "controls"

    child_names = \
        ['acoustics_wave_equation_controls', 'advanced',
         'contact_solution_controls', 'courant_number', 'equations', 'limits',
         'p_v_controls', 'relaxation_factor', 'set_controls_to_default',
         'under_relaxation']

    _child_classes = dict(
        acoustics_wave_equation_controls=acoustics_wave_equation_controls_cls,
        advanced=advanced_cls,
        contact_solution_controls=contact_solution_controls_cls,
        courant_number=courant_number_cls,
        equations=equations_cls,
        limits=limits_cls,
        p_v_controls=p_v_controls_cls,
        relaxation_factor=relaxation_factor_cls,
        set_controls_to_default=set_controls_to_default_cls,
        under_relaxation=under_relaxation_cls,
    )

