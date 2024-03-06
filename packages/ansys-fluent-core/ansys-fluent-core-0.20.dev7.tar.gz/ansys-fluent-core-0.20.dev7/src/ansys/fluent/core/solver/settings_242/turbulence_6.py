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

from .rough_bc import rough_bc as rough_bc_cls
from .rough_option import rough_option as rough_option_cls
from .rough_nasa import rough_nasa as rough_nasa_cls
from .rough_shin_et_al import rough_shin_et_al as rough_shin_et_al_cls
from .rough_data import rough_data as rough_data_cls
from .roughness_height import roughness_height as roughness_height_cls
from .roughness_const import roughness_const as roughness_const_cls
from .roughness_height_cp import roughness_height_cp as roughness_height_cp_cls
from .roughness_const_cp import roughness_const_cp as roughness_const_cp_cls
from .roughness_const_nasa import roughness_const_nasa as roughness_const_nasa_cls
from .roughness_const_shin import roughness_const_shin as roughness_const_shin_cls
from .roughness_const_data import roughness_const_data as roughness_const_data_cls
from .variable_roughness import variable_roughness as variable_roughness_cls
from .free_stream_velocity import free_stream_velocity as free_stream_velocity_cls
from .free_stream_temp import free_stream_temp as free_stream_temp_cls
from .characteristic_length import characteristic_length as characteristic_length_cls
from .free_stream_temp_cp import free_stream_temp_cp as free_stream_temp_cp_cls
from .characteristic_length_cp import characteristic_length_cp as characteristic_length_cp_cls
from .liquid_content import liquid_content as liquid_content_cls
from .liquid_content_cp import liquid_content_cp as liquid_content_cp_cls
from .droplet_diameter import droplet_diameter as droplet_diameter_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['rough_bc', 'rough_option', 'rough_nasa', 'rough_shin_et_al',
         'rough_data', 'roughness_height', 'roughness_const',
         'roughness_height_cp', 'roughness_const_cp', 'roughness_const_nasa',
         'roughness_const_shin', 'roughness_const_data', 'variable_roughness',
         'free_stream_velocity', 'free_stream_temp', 'characteristic_length',
         'free_stream_temp_cp', 'characteristic_length_cp', 'liquid_content',
         'liquid_content_cp', 'droplet_diameter']

    _child_classes = dict(
        rough_bc=rough_bc_cls,
        rough_option=rough_option_cls,
        rough_nasa=rough_nasa_cls,
        rough_shin_et_al=rough_shin_et_al_cls,
        rough_data=rough_data_cls,
        roughness_height=roughness_height_cls,
        roughness_const=roughness_const_cls,
        roughness_height_cp=roughness_height_cp_cls,
        roughness_const_cp=roughness_const_cp_cls,
        roughness_const_nasa=roughness_const_nasa_cls,
        roughness_const_shin=roughness_const_shin_cls,
        roughness_const_data=roughness_const_data_cls,
        variable_roughness=variable_roughness_cls,
        free_stream_velocity=free_stream_velocity_cls,
        free_stream_temp=free_stream_temp_cls,
        characteristic_length=characteristic_length_cls,
        free_stream_temp_cp=free_stream_temp_cp_cls,
        characteristic_length_cp=characteristic_length_cp_cls,
        liquid_content=liquid_content_cls,
        liquid_content_cp=liquid_content_cp_cls,
        droplet_diameter=droplet_diameter_cls,
    )

