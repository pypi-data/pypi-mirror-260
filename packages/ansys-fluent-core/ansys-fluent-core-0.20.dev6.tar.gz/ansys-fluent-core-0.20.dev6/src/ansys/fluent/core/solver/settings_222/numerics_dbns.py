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

from .first_to_second_order_blending_dbns import first_to_second_order_blending_dbns as first_to_second_order_blending_dbns_cls
class numerics_dbns(Group):
    """
    'numerics_dbns' child.
    """

    fluent_name = "numerics-dbns"

    child_names = \
        ['first_to_second_order_blending_dbns']

    _child_classes = dict(
        first_to_second_order_blending_dbns=first_to_second_order_blending_dbns_cls,
    )

