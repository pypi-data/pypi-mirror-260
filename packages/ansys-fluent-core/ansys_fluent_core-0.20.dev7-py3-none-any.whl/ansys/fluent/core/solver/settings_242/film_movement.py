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

from .condensing_film_stationary import condensing_film_stationary as condensing_film_stationary_cls
from .all_film_stationary import all_film_stationary as all_film_stationary_cls
class film_movement(Group):
    """
    Set options for controlling the film particles movement.
    """

    fluent_name = "film-movement"

    child_names = \
        ['condensing_film_stationary', 'all_film_stationary']

    _child_classes = dict(
        condensing_film_stationary=condensing_film_stationary_cls,
        all_film_stationary=all_film_stationary_cls,
    )

