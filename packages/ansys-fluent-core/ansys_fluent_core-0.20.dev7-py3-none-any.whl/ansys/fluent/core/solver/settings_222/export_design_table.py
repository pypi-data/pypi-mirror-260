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

from .filepath import filepath as filepath_cls
class export_design_table(Command):
    """
    Export Design Point Table.
    
    Parameters
    ----------
        filepath : str
            'filepath' child.
    
    """

    fluent_name = "export-design-table"

    argument_names = \
        ['filepath']

    _child_classes = dict(
        filepath=filepath_cls,
    )

