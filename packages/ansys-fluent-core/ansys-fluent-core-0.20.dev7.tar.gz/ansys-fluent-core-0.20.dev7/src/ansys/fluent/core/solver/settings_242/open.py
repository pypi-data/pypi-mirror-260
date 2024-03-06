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

from .project_filename_1 import project_filename_1 as project_filename_1_cls
from .load_case import load_case as load_case_cls
class open(Command):
    """
    Open project.
    
    Parameters
    ----------
        project_filename_1 : str
            'project_filename' child.
        load_case : bool
            'load_case' child.
    
    """

    fluent_name = "open"

    argument_names = \
        ['project_filename', 'load_case']

    _child_classes = dict(
        project_filename=project_filename_1_cls,
        load_case=load_case_cls,
    )

