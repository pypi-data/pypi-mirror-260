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

from .eload_settings import eload_settings as eload_settings_cls
from .echem_stop_criterion import echem_stop_criterion as echem_stop_criterion_cls
class eload_condition(Group):
    """
    Set up electric load conditions.
    """

    fluent_name = "eload-condition"

    child_names = \
        ['eload_settings', 'echem_stop_criterion']

    _child_classes = dict(
        eload_settings=eload_settings_cls,
        echem_stop_criterion=echem_stop_criterion_cls,
    )

