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

from .motion_bc import motion_bc as motion_bc_cls
from .shear_bc import shear_bc as shear_bc_cls
from .moving import moving as moving_cls
from .relative import relative as relative_cls
from .rotating import rotating as rotating_cls
from .vmag import vmag as vmag_cls
from .wall_translation import wall_translation as wall_translation_cls
from .components_1 import components as components_cls
from .velocity_2 import velocity as velocity_cls
from .fsi_interface import fsi_interface as fsi_interface_cls
from .periodic_displacement import periodic_displacement as periodic_displacement_cls
from .periodic_imaginary_displacement import periodic_imaginary_displacement as periodic_imaginary_displacement_cls
from .freq import freq as freq_cls
from .amp import amp as amp_cls
from .nodal_diam import nodal_diam as nodal_diam_cls
from .pass_number import pass_number as pass_number_cls
from .fwd import fwd as fwd_cls
from .aero import aero as aero_cls
from .cmplx import cmplx as cmplx_cls
from .norm import norm as norm_cls
from .method_5 import method as method_cls
from .omega_1 import omega as omega_cls
from .rotation_axis_origin import rotation_axis_origin as rotation_axis_origin_cls
from .rotation_axis_direction import rotation_axis_direction as rotation_axis_direction_cls
from .specified_shear import specified_shear as specified_shear_cls
from .shear_stress import shear_stress as shear_stress_cls
from .fslip import fslip as fslip_cls
from .eslip import eslip as eslip_cls
from .surf_tens_grad import surf_tens_grad as surf_tens_grad_cls
from .specular_coeff import specular_coeff as specular_coeff_cls
from .mom_accom_coef import mom_accom_coef as mom_accom_coef_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['motion_bc', 'shear_bc', 'moving', 'relative', 'rotating', 'vmag',
         'wall_translation', 'components', 'velocity', 'fsi_interface',
         'periodic_displacement', 'periodic_imaginary_displacement', 'freq',
         'amp', 'nodal_diam', 'pass_number', 'fwd', 'aero', 'cmplx', 'norm',
         'method', 'omega', 'rotation_axis_origin', 'rotation_axis_direction',
         'specified_shear', 'shear_stress', 'fslip', 'eslip',
         'surf_tens_grad', 'specular_coeff', 'mom_accom_coef']

    _child_classes = dict(
        motion_bc=motion_bc_cls,
        shear_bc=shear_bc_cls,
        moving=moving_cls,
        relative=relative_cls,
        rotating=rotating_cls,
        vmag=vmag_cls,
        wall_translation=wall_translation_cls,
        components=components_cls,
        velocity=velocity_cls,
        fsi_interface=fsi_interface_cls,
        periodic_displacement=periodic_displacement_cls,
        periodic_imaginary_displacement=periodic_imaginary_displacement_cls,
        freq=freq_cls,
        amp=amp_cls,
        nodal_diam=nodal_diam_cls,
        pass_number=pass_number_cls,
        fwd=fwd_cls,
        aero=aero_cls,
        cmplx=cmplx_cls,
        norm=norm_cls,
        method=method_cls,
        omega=omega_cls,
        rotation_axis_origin=rotation_axis_origin_cls,
        rotation_axis_direction=rotation_axis_direction_cls,
        specified_shear=specified_shear_cls,
        shear_stress=shear_stress_cls,
        fslip=fslip_cls,
        eslip=eslip_cls,
        surf_tens_grad=surf_tens_grad_cls,
        specular_coeff=specular_coeff_cls,
        mom_accom_coef=mom_accom_coef_cls,
    )

