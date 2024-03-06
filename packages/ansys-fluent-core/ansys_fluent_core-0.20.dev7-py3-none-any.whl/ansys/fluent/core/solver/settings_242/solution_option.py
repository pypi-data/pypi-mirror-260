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

from .option_settings import option_settings as option_settings_cls
from .cell_clustering import cell_clustering as cell_clustering_cls
class solution_option(Group):
    """
    Solution options.
    """

    fluent_name = "solution-option"

    child_names = \
        ['option_settings', 'cell_clustering']

    _child_classes = dict(
        option_settings=option_settings_cls,
        cell_clustering=cell_clustering_cls,
    )

