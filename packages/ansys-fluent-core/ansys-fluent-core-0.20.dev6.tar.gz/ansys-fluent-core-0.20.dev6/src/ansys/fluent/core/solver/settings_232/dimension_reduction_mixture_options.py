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

from .number_of_represented_species import number_of_represented_species as number_of_represented_species_cls
from .full_mechanism_material_name import full_mechanism_material_name as full_mechanism_material_name_cls
from .fuel_oxidizer_species import fuel_oxidizer_species as fuel_oxidizer_species_cls
class dimension_reduction_mixture_options(Group):
    """
    'dimension_reduction_mixture_options' child.
    """

    fluent_name = "dimension-reduction-mixture-options"

    child_names = \
        ['number_of_represented_species', 'full_mechanism_material_name',
         'fuel_oxidizer_species']

    _child_classes = dict(
        number_of_represented_species=number_of_represented_species_cls,
        full_mechanism_material_name=full_mechanism_material_name_cls,
        fuel_oxidizer_species=fuel_oxidizer_species_cls,
    )

