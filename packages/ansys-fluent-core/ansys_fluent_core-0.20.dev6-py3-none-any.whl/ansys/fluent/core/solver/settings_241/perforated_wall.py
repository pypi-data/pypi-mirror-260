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

from .setup_method import setup_method as setup_method_cls
from .model_setup import model_setup as model_setup_cls
from .read_input_file import read_input_file as read_input_file_cls
class perforated_wall(Group):
    """
    Perforated wall model.
    """

    fluent_name = "perforated-wall"

    child_names = \
        ['setup_method', 'model_setup']

    command_names = \
        ['read_input_file']

    _child_classes = dict(
        setup_method=setup_method_cls,
        model_setup=model_setup_cls,
        read_input_file=read_input_file_cls,
    )

