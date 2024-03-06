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

from .enabled_18 import enabled as enabled_cls
from .model_type import model_type as model_type_cls
from .only_abuse import only_abuse as only_abuse_cls
from .one_equation import one_equation as one_equation_cls
from .four_equation import four_equation as four_equation_cls
from .internal_short import internal_short as internal_short_cls
class thermal_abuse_model(Group):
    """
    Set thermal abuse model related parameters.
    """

    fluent_name = "thermal-abuse-model"

    child_names = \
        ['enabled', 'model_type', 'only_abuse', 'one_equation',
         'four_equation', 'internal_short']

    _child_classes = dict(
        enabled=enabled_cls,
        model_type=model_type_cls,
        only_abuse=only_abuse_cls,
        one_equation=one_equation_cls,
        four_equation=four_equation_cls,
        internal_short=internal_short_cls,
    )

