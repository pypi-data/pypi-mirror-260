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

from .ninjections import ninjections as ninjections_cls
from .urf import urf as urf_cls
from .injection import injection as injection_cls
class model_setup(Group):
    """
    'model_setup' child.
    """

    fluent_name = "model-setup"

    child_names = \
        ['ninjections', 'urf', 'injection']

    _child_classes = dict(
        ninjections=ninjections_cls,
        urf=urf_cls,
        injection=injection_cls,
    )

