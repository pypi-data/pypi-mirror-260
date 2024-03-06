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

from .output_quantity import output_quantity as output_quantity_cls
from .rotor_name import rotor_name as rotor_name_cls
from .scale_output import scale_output as scale_output_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append import append as append_cls
class vbm(Command):
    """
    'vbm' command.
    
    Parameters
    ----------
        output_quantity : str
            'output_quantity' child.
        rotor_name : str
            'rotor_name' child.
        scale_output : bool
            'scale_output' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append : bool
            'append' child.
    
    """

    fluent_name = "vbm"

    argument_names = \
        ['output_quantity', 'rotor_name', 'scale_output', 'write_to_file',
         'file_name', 'append']

    _child_classes = dict(
        output_quantity=output_quantity_cls,
        rotor_name=rotor_name_cls,
        scale_output=scale_output_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append=append_cls,
    )

