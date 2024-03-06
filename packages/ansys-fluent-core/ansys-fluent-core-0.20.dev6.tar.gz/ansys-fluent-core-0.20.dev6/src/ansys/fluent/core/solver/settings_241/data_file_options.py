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

from .reset_defined_derived_quantities import reset_defined_derived_quantities as reset_defined_derived_quantities_cls
from .derived_quantities import derived_quantities as derived_quantities_cls
class data_file_options(Command):
    """
    Set derived quantities to be written in data file.
    
    Parameters
    ----------
        reset_defined_derived_quantities : bool
            'reset_defined_derived_quantities' child.
        derived_quantities : typing.List[str]
            'derived_quantities' child.
    
    """

    fluent_name = "data-file-options"

    argument_names = \
        ['reset_defined_derived_quantities', 'derived_quantities']

    _child_classes = dict(
        reset_defined_derived_quantities=reset_defined_derived_quantities_cls,
        derived_quantities=derived_quantities_cls,
    )

