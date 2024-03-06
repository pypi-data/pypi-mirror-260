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

from .deactivate_cell_zone import deactivate_cell_zone as deactivate_cell_zone_cls
from .delete_cell_zone import delete_cell_zone as delete_cell_zone_cls
from .copy_move_cell_zone import copy_move_cell_zone as copy_move_cell_zone_cls
from .list_zones import list_zones as list_zones_cls
from .extrude_face_zone_delta import extrude_face_zone_delta as extrude_face_zone_delta_cls
from .extrude_face_zone_para import extrude_face_zone_para as extrude_face_zone_para_cls
from .fuse_face_zones import fuse_face_zones as fuse_face_zones_cls
from .scale_zone import scale_zone as scale_zone_cls
from .rotate_zone import rotate_zone as rotate_zone_cls
from .translate_zone import translate_zone as translate_zone_cls
from .merge_zones import merge_zones as merge_zones_cls
from .replace_zone import replace_zone as replace_zone_cls
from .append_mesh import append_mesh as append_mesh_cls
from .append_mesh_data import append_mesh_data as append_mesh_data_cls
from .sep_cell_zone_mark import sep_cell_zone_mark as sep_cell_zone_mark_cls
from .sep_cell_zone_region import sep_cell_zone_region as sep_cell_zone_region_cls
from .sep_face_zone_angle import sep_face_zone_angle as sep_face_zone_angle_cls
from .sep_face_zone_face import sep_face_zone_face as sep_face_zone_face_cls
from .sep_face_zone_mark import sep_face_zone_mark as sep_face_zone_mark_cls
from .sep_face_zone_region import sep_face_zone_region as sep_face_zone_region_cls
from .zone_name_2 import zone_name as zone_name_cls
from .change_zone_state import change_zone_state as change_zone_state_cls
from .make_periodic import make_periodic as make_periodic_cls
from .create_periodic_interface import create_periodic_interface as create_periodic_interface_cls
from .slit_periodic_1 import slit_periodic as slit_periodic_cls
from .zone_type import zone_type as zone_type_cls
class modify_zones(Group):
    """
    Enter the modify zones menu.
    """

    fluent_name = "modify-zones"

    command_names = \
        ['deactivate_cell_zone', 'delete_cell_zone', 'copy_move_cell_zone',
         'list_zones', 'extrude_face_zone_delta', 'extrude_face_zone_para',
         'fuse_face_zones', 'scale_zone', 'rotate_zone', 'translate_zone',
         'merge_zones', 'replace_zone', 'append_mesh', 'append_mesh_data',
         'sep_cell_zone_mark', 'sep_cell_zone_region', 'sep_face_zone_angle',
         'sep_face_zone_face', 'sep_face_zone_mark', 'sep_face_zone_region',
         'zone_name', 'change_zone_state', 'make_periodic',
         'create_periodic_interface', 'slit_periodic', 'zone_type']

    _child_classes = dict(
        deactivate_cell_zone=deactivate_cell_zone_cls,
        delete_cell_zone=delete_cell_zone_cls,
        copy_move_cell_zone=copy_move_cell_zone_cls,
        list_zones=list_zones_cls,
        extrude_face_zone_delta=extrude_face_zone_delta_cls,
        extrude_face_zone_para=extrude_face_zone_para_cls,
        fuse_face_zones=fuse_face_zones_cls,
        scale_zone=scale_zone_cls,
        rotate_zone=rotate_zone_cls,
        translate_zone=translate_zone_cls,
        merge_zones=merge_zones_cls,
        replace_zone=replace_zone_cls,
        append_mesh=append_mesh_cls,
        append_mesh_data=append_mesh_data_cls,
        sep_cell_zone_mark=sep_cell_zone_mark_cls,
        sep_cell_zone_region=sep_cell_zone_region_cls,
        sep_face_zone_angle=sep_face_zone_angle_cls,
        sep_face_zone_face=sep_face_zone_face_cls,
        sep_face_zone_mark=sep_face_zone_mark_cls,
        sep_face_zone_region=sep_face_zone_region_cls,
        zone_name=zone_name_cls,
        change_zone_state=change_zone_state_cls,
        make_periodic=make_periodic_cls,
        create_periodic_interface=create_periodic_interface_cls,
        slit_periodic=slit_periodic_cls,
        zone_type=zone_type_cls,
    )

