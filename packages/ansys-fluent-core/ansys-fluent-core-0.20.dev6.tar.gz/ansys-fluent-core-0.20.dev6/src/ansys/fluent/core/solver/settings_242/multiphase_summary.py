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

from .verbosity_option import verbosity_option as verbosity_option_cls
class multiphase_summary(Command):
    """
    Multiphase Summary and Recommendations.
    
    Parameters
    ----------
        verbosity_option : str
            'verbosity_option' child.
    
    """

    fluent_name = "multiphase-summary"

    argument_names = \
        ['verbosity_option']

    _child_classes = dict(
        verbosity_option=verbosity_option_cls,
    )

