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

from .postprocess_options import postprocess_options as postprocess_options_cls
from .monitors import monitors as monitors_cls
from .methods_2 import methods as methods_cls
from .controls_2 import controls as controls_cls
from .calculation import calculation as calculation_cls
from .observables import observables as observables_cls
from .reporting import reporting as reporting_cls
from .enable_21 import enable as enable_cls
class gradient_based(Group):
    """
    Gradient-based design menu.
    """

    fluent_name = "gradient-based"

    child_names = \
        ['postprocess_options', 'monitors', 'methods', 'controls',
         'calculation', 'observables', 'reporting']

    command_names = \
        ['enable']

    _child_classes = dict(
        postprocess_options=postprocess_options_cls,
        monitors=monitors_cls,
        methods=methods_cls,
        controls=controls_cls,
        calculation=calculation_cls,
        observables=observables_cls,
        reporting=reporting_cls,
        enable=enable_cls,
    )

