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

class sa_enhanced_wall_treatment(Boolean):
    """
    Enable/disable the enhanced wall treatment for the Spalart-Allmaras model.
    If disabled, no smooth blending between the viscous sublayer and the
    log-law formulation is employed, as was done in versions previous to Fluent14.
    """

    fluent_name = "sa-enhanced-wall-treatment?"

