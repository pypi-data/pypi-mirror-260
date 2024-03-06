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

from .project_filename import project_filename as project_filename_cls
class initialize(Command):
    """
    Start Parametric Study.
    
    Parameters
    ----------
        project_filename : str
            'project_filename' child.
    
    """

    fluent_name = "initialize"

    argument_names = \
        ['project_filename']

    _child_classes = dict(
        project_filename=project_filename_cls,
    )

