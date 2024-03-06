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

from .mesh_1 import mesh as mesh_cls
from .surface_1 import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .time_1 import time as time_cls
from .flux_1 import flux as flux_cls
from .injection_1 import injection as injection_cls
from .user_defined_5 import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .icing_3 import icing as icing_cls
from .expression_1 import expression as expression_cls
from .single_valued_expression import single_valued_expression as single_valued_expression_cls
from .custom import custom as custom_cls
from .compute_2 import compute as compute_cls
from .copy_2 import copy as copy_cls
class report_definitions(Group, _ChildNamedObjectAccessorMixin):
    """
    'report_definitions' child.
    """

    fluent_name = "report-definitions"

    child_names = \
        ['mesh', 'surface', 'volume', 'force', 'lift', 'drag', 'moment',
         'time', 'flux', 'injection', 'user_defined', 'aeromechanics',
         'icing', 'expression', 'single_valued_expression', 'custom']

    command_names = \
        ['compute', 'copy']

    _child_classes = dict(
        mesh=mesh_cls,
        surface=surface_cls,
        volume=volume_cls,
        force=force_cls,
        lift=lift_cls,
        drag=drag_cls,
        moment=moment_cls,
        time=time_cls,
        flux=flux_cls,
        injection=injection_cls,
        user_defined=user_defined_cls,
        aeromechanics=aeromechanics_cls,
        icing=icing_cls,
        expression=expression_cls,
        single_valued_expression=single_valued_expression_cls,
        custom=custom_cls,
        compute=compute_cls,
        copy=copy_cls,
    )

