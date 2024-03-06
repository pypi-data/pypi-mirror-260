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

from .iter_per_coupling_count import iter_per_coupling_count as iter_per_coupling_count_cls
from .single_session_coupling import single_session_coupling as single_session_coupling_cls
from .two_session_coupling import two_session_coupling as two_session_coupling_cls
class coupling(Group):
    """
    'coupling' child.
    """

    fluent_name = "coupling"

    child_names = \
        ['iter_per_coupling_count', 'single_session_coupling',
         'two_session_coupling']

    _child_classes = dict(
        iter_per_coupling_count=iter_per_coupling_count_cls,
        single_session_coupling=single_session_coupling_cls,
        two_session_coupling=two_session_coupling_cls,
    )

