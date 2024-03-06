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

from .filename_1 import filename as filename_cls
class import_modifications(Command):
    """
    Import a list of case modifications from a tsv file.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "import-modifications"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

