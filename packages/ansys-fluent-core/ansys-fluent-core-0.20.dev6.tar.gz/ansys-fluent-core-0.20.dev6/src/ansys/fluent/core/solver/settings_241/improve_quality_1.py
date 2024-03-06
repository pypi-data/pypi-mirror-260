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

from .check_mapped_interface_quality import check_mapped_interface_quality as check_mapped_interface_quality_cls
from .continue_ import continue_ as continue__cls
from .tol_percentage_increment import tol_percentage_increment as tol_percentage_increment_cls
class improve_quality(Command):
    """
    Improve mesh interface quality.
    
    Parameters
    ----------
        check_mapped_interface_quality : bool
            Check Mapped Interface Qaulity.
        continue_ : bool
            Continue to improve the mapped interface quality.
        tol_percentage_increment : real
            'tol_percentage_increment' child.
    
    """

    fluent_name = "improve-quality"

    argument_names = \
        ['check_mapped_interface_quality', 'continue_',
         'tol_percentage_increment']

    _child_classes = dict(
        check_mapped_interface_quality=check_mapped_interface_quality_cls,
        continue_=continue__cls,
        tol_percentage_increment=tol_percentage_increment_cls,
    )

