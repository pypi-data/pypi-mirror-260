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

from .pole_real import pole_real as pole_real_cls
from .pole_imag import pole_imag as pole_imag_cls
from .amplitude_real import amplitude_real as amplitude_real_cls
from .amplitude_imag import amplitude_imag as amplitude_imag_cls
class impedance_2_child(Group):
    """
    'child_object_type' of impedance_2.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole_real', 'pole_imag', 'amplitude_real', 'amplitude_imag']

    _child_classes = dict(
        pole_real=pole_real_cls,
        pole_imag=pole_imag_cls,
        amplitude_real=amplitude_real_cls,
        amplitude_imag=amplitude_imag_cls,
    )

