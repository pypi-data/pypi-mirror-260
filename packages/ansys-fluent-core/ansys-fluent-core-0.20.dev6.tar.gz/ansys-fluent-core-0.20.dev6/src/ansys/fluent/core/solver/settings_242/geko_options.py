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

from .wall_distance_free import wall_distance_free as wall_distance_free_cls
from .version import version as version_cls
from .cjet import cjet as cjet_cls
from .creal import creal as creal_cls
from .cnw_sub import cnw_sub as cnw_sub_cls
from .cjet_aux import cjet_aux as cjet_aux_cls
from .cbf_lam import cbf_lam as cbf_lam_cls
from .cbf_tur import cbf_tur as cbf_tur_cls
from .geko_defaults import geko_defaults as geko_defaults_cls
class geko_options(Group):
    """
    'geko_options' child.
    """

    fluent_name = "geko-options"

    child_names = \
        ['wall_distance_free', 'version', 'cjet', 'creal', 'cnw_sub',
         'cjet_aux', 'cbf_lam', 'cbf_tur']

    command_names = \
        ['geko_defaults']

    _child_classes = dict(
        wall_distance_free=wall_distance_free_cls,
        version=version_cls,
        cjet=cjet_cls,
        creal=creal_cls,
        cnw_sub=cnw_sub_cls,
        cjet_aux=cjet_aux_cls,
        cbf_lam=cbf_lam_cls,
        cbf_tur=cbf_tur_cls,
        geko_defaults=geko_defaults_cls,
    )

