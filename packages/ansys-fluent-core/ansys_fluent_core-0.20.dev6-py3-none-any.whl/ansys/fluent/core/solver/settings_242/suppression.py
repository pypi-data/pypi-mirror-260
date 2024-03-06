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

class suppression(Boolean):
    """
    As part of the dissipation scheme, the growth of instabilities is stopped by the effect of the dissipation.Enabling the Suppression option ensures that these undesirable patterns will then also decay as the calculation progresses.
    """

    fluent_name = "suppression"

