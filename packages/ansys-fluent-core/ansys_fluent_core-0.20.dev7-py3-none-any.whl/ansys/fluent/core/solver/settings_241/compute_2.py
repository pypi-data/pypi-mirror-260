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

from .report_defs import report_defs as report_defs_cls
class compute(Command):
    """
    'compute' command.
    
    Parameters
    ----------
        report_defs : typing.List[str]
            'report_defs' child.
    
    """

    fluent_name = "compute"

    argument_names = \
        ['report_defs']

    _child_classes = dict(
        report_defs=report_defs_cls,
    )

