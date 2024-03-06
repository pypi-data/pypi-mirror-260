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

from .courant_number_reduction import courant_number_reduction as courant_number_reduction_cls
from .correction_reduction import correction_reduction as correction_reduction_cls
from .correction_smoothing import correction_smoothing as correction_smoothing_cls
from .species_correction_reduction import species_correction_reduction as species_correction_reduction_cls
class relaxation_factor(Group):
    """
    Enter FAS multigrid relaxation factor menu.
    """

    fluent_name = "relaxation-factor"

    child_names = \
        ['courant_number_reduction', 'correction_reduction',
         'correction_smoothing', 'species_correction_reduction']

    _child_classes = dict(
        courant_number_reduction=courant_number_reduction_cls,
        correction_reduction=correction_reduction_cls,
        correction_smoothing=correction_smoothing_cls,
        species_correction_reduction=species_correction_reduction_cls,
    )

