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

from .udf_cf_names import udf_cf_names as udf_cf_names_cls
class setup_unsteady_statistics(Command):
    """
    'setup_unsteady_statistics' command.
    
    Parameters
    ----------
        udf_cf_names : typing.List[str]
            'udf_cf_names' child.
    
    """

    fluent_name = "setup-unsteady-statistics"

    argument_names = \
        ['udf_cf_names']

    _child_classes = dict(
        udf_cf_names=udf_cf_names_cls,
    )

