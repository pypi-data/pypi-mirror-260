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

from .separate_journals import separate_journals as separate_journals_cls
class save_journals(Command):
    """
    Save Journals.
    
    Parameters
    ----------
        separate_journals : bool
            'separate_journals' child.
    
    """

    fluent_name = "save-journals"

    argument_names = \
        ['separate_journals']

    _child_classes = dict(
        separate_journals=separate_journals_cls,
    )

