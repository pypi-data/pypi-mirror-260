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

from .enable_11 import enable as enable_cls
from .sources import sources as sources_cls
class source_terms(Group):
    """
    Help not available.
    """

    fluent_name = "source-terms"

    child_names = \
        ['enable', 'sources']

    _child_classes = dict(
        enable=enable_cls,
        sources=sources_cls,
    )

