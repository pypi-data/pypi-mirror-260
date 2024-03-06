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

from .lti_folder_name import lti_folder_name as lti_folder_name_cls
from .user_config import user_config as user_config_cls
from .min_order import min_order as min_order_cls
from .max_order import max_order as max_order_cls
from .rel_error import rel_error as rel_error_cls
from .tolerance_0th_order import tolerance_0th_order as tolerance_0th_order_cls
from .slope_method import slope_method as slope_method_cls
from .run_rom_generation import run_rom_generation as run_rom_generation_cls
class lti_rom_generation(Group):
    """
    LTI-ROM Generator command.
    """

    fluent_name = "lti-rom-generation"

    child_names = \
        ['lti_folder_name', 'user_config', 'min_order', 'max_order',
         'rel_error', 'tolerance_0th_order', 'slope_method']

    command_names = \
        ['run_rom_generation']

    _child_classes = dict(
        lti_folder_name=lti_folder_name_cls,
        user_config=user_config_cls,
        min_order=min_order_cls,
        max_order=max_order_cls,
        rel_error=rel_error_cls,
        tolerance_0th_order=tolerance_0th_order_cls,
        slope_method=slope_method_cls,
        run_rom_generation=run_rom_generation_cls,
    )

