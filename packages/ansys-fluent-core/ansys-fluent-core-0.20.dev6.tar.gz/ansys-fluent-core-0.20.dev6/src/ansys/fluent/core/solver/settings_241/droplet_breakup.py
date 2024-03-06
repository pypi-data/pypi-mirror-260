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

from .option import option as option_cls
from .y0 import y0 as y0_cls
from .number_of_child_droplets import number_of_child_droplets as number_of_child_droplets_cls
from .b1 import b1 as b1_cls
from .b0 import b0 as b0_cls
from .cl import cl as cl_cls
from .ctau import ctau as ctau_cls
from .crt import crt as crt_cls
from .critical_weber_number import critical_weber_number as critical_weber_number_cls
from .core_b1 import core_b1 as core_b1_cls
from .xi import xi as xi_cls
from .target_number_in_parcel import target_number_in_parcel as target_number_in_parcel_cls
from .c0 import c0 as c0_cls
from .column_drag_coeff import column_drag_coeff as column_drag_coeff_cls
from .ligament_factor import ligament_factor as ligament_factor_cls
from .jet_diameter import jet_diameter as jet_diameter_cls
from .k1 import k1 as k1_cls
from .k2 import k2 as k2_cls
from .tb import tb as tb_cls
class droplet_breakup(Group):
    """
    'droplet_breakup' child.
    """

    fluent_name = "droplet-breakup"

    child_names = \
        ['option', 'y0', 'number_of_child_droplets', 'b1', 'b0', 'cl', 'ctau',
         'crt', 'critical_weber_number', 'core_b1', 'xi',
         'target_number_in_parcel', 'c0', 'column_drag_coeff',
         'ligament_factor', 'jet_diameter', 'k1', 'k2', 'tb']

    _child_classes = dict(
        option=option_cls,
        y0=y0_cls,
        number_of_child_droplets=number_of_child_droplets_cls,
        b1=b1_cls,
        b0=b0_cls,
        cl=cl_cls,
        ctau=ctau_cls,
        crt=crt_cls,
        critical_weber_number=critical_weber_number_cls,
        core_b1=core_b1_cls,
        xi=xi_cls,
        target_number_in_parcel=target_number_in_parcel_cls,
        c0=c0_cls,
        column_drag_coeff=column_drag_coeff_cls,
        ligament_factor=ligament_factor_cls,
        jet_diameter=jet_diameter_cls,
        k1=k1_cls,
        k2=k2_cls,
        tb=tb_cls,
    )

