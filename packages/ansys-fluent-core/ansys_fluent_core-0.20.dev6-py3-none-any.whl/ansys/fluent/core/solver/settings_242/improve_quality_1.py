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
from .proceed_1 import proceed as proceed_cls
from .tol_percentage_increment import tol_percentage_increment as tol_percentage_increment_cls
class improve_quality(Command):
    """
    Improve mesh interface quality.
    
    Parameters
    ----------
        check_mapped_interface_quality : bool
            Check Mapped Interface Qaulity.
        proceed : bool
            Continue to improve the mapped interface quality.
        tol_percentage_increment : real
            Enter a percentage increment for tolerance (%).
    
    """

    fluent_name = "improve-quality"

    argument_names = \
        ['check_mapped_interface_quality', 'proceed',
         'tol_percentage_increment']

    _child_classes = dict(
        check_mapped_interface_quality=check_mapped_interface_quality_cls,
        proceed=proceed_cls,
        tol_percentage_increment=tol_percentage_increment_cls,
    )

