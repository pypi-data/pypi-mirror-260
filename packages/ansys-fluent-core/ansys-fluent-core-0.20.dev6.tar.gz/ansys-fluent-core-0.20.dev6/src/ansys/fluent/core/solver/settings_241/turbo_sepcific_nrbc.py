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

from .enable_10 import enable as enable_cls
from .discretization import discretization as discretization_cls
from .under_relaxation_1 import under_relaxation as under_relaxation_cls
from .verbosity_5 import verbosity as verbosity_cls
from .initialize import initialize as initialize_cls
from .show_status import show_status as show_status_cls
class turbo_sepcific_nrbc(Group):
    """
    'turbo_sepcific_nrbc' child.
    """

    fluent_name = "turbo-sepcific-nrbc"

    child_names = \
        ['enable', 'discretization', 'under_relaxation', 'verbosity']

    command_names = \
        ['initialize', 'show_status']

    _child_classes = dict(
        enable=enable_cls,
        discretization=discretization_cls,
        under_relaxation=under_relaxation_cls,
        verbosity=verbosity_cls,
        initialize=initialize_cls,
        show_status=show_status_cls,
    )

