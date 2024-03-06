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

from .averaging import averaging as averaging_cls
from .source_terms import source_terms as source_terms_cls
from .tracking import tracking as tracking_cls
from .parcel_count_control import parcel_count_control as parcel_count_control_cls
class numerics(Group):
    """
    Main menu to allow users to set options controlling the solution of ordinary differential equations describing 
    the underlying physics of the Discrete Phase Model.
    For more details consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "numerics"

    child_names = \
        ['averaging', 'source_terms', 'tracking', 'parcel_count_control']

    _child_classes = dict(
        averaging=averaging_cls,
        source_terms=source_terms_cls,
        tracking=tracking_cls,
        parcel_count_control=parcel_count_control_cls,
    )

