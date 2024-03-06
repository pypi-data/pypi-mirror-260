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

from .solution_stabilization import solution_stabilization as solution_stabilization_cls
from .verbosity_1 import verbosity as verbosity_cls
from .parameters import parameters as parameters_cls
from .spatial import spatial as spatial_cls
from .transient import transient as transient_cls
from .amg import amg as amg_cls
from .models_2 import models as models_cls
from .methods import methods as methods_cls
from .miscellaneous import miscellaneous as miscellaneous_cls
from .set_settings_to_default import set_settings_to_default as set_settings_to_default_cls
class contact_solution_controls(Group):
    """
    'contact_solution_controls' child.
    """

    fluent_name = "contact-solution-controls"

    child_names = \
        ['solution_stabilization', 'verbosity', 'parameters', 'spatial',
         'transient', 'amg', 'models', 'methods', 'miscellaneous']

    command_names = \
        ['set_settings_to_default']

    _child_classes = dict(
        solution_stabilization=solution_stabilization_cls,
        verbosity=verbosity_cls,
        parameters=parameters_cls,
        spatial=spatial_cls,
        transient=transient_cls,
        amg=amg_cls,
        models=models_cls,
        methods=methods_cls,
        miscellaneous=miscellaneous_cls,
        set_settings_to_default=set_settings_to_default_cls,
    )

