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

from .particle_type import particle_type as particle_type_cls
from .material import material as material_cls
from .reference_frame import reference_frame as reference_frame_cls
from .number_of_streams import number_of_streams as number_of_streams_cls
from .injection_type import injection_type as injection_type_cls
from .interaction_1 import interaction as interaction_cls
from .parcel_method import parcel_method as parcel_method_cls
from .particle_reinjector import particle_reinjector as particle_reinjector_cls
from .physical_models import physical_models as physical_models_cls
from .initial_props import initial_props as initial_props_cls
class injections_child(Group):
    """
    'child_object_type' of injections.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['particle_type', 'material', 'reference_frame', 'number_of_streams',
         'injection_type', 'interaction', 'parcel_method',
         'particle_reinjector', 'physical_models', 'initial_props']

    _child_classes = dict(
        particle_type=particle_type_cls,
        material=material_cls,
        reference_frame=reference_frame_cls,
        number_of_streams=number_of_streams_cls,
        injection_type=injection_type_cls,
        interaction=interaction_cls,
        parcel_method=parcel_method_cls,
        particle_reinjector=particle_reinjector_cls,
        physical_models=physical_models_cls,
        initial_props=initial_props_cls,
    )

