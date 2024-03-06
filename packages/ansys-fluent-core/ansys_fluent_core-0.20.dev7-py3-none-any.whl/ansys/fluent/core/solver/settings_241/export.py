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

from .sc_def_file_settings import sc_def_file_settings as sc_def_file_settings_cls
from .settings import settings as settings_cls
from .abaqus import abaqus as abaqus_cls
from .mechanical_apdl import mechanical_apdl as mechanical_apdl_cls
from .mechanical_apdl_input import mechanical_apdl_input as mechanical_apdl_input_cls
from .ascii import ascii as ascii_cls
from .avs import avs as avs_cls
from .ensight import ensight as ensight_cls
from .ensight_gold import ensight_gold as ensight_gold_cls
from .fieldview import fieldview as fieldview_cls
from .fieldview_data import fieldview_data as fieldview_data_cls
from .gambit import gambit as gambit_cls
from .cgns import cgns as cgns_cls
from .custom_heat_flux import custom_heat_flux as custom_heat_flux_cls
from .dx import dx as dx_cls
from .ensight_gold_parallel_surfaces import ensight_gold_parallel_surfaces as ensight_gold_parallel_surfaces_cls
from .ensight_gold_parallel_volume import ensight_gold_parallel_volume as ensight_gold_parallel_volume_cls
from .icemcfd_for_icepak import icemcfd_for_icepak as icemcfd_for_icepak_cls
from .fast_mesh import fast_mesh as fast_mesh_cls
from .fast_solution import fast_solution as fast_solution_cls
from .fast_velocity import fast_velocity as fast_velocity_cls
from .taitherm import taitherm as taitherm_cls
from .fieldview_unstruct import fieldview_unstruct as fieldview_unstruct_cls
from .fieldview_unstruct_mesh import fieldview_unstruct_mesh as fieldview_unstruct_mesh_cls
from .fieldview_unstruct_data import fieldview_unstruct_data as fieldview_unstruct_data_cls
from .fieldview_unstruct_surfaces import fieldview_unstruct_surfaces as fieldview_unstruct_surfaces_cls
from .ideas import ideas as ideas_cls
from .nastran import nastran as nastran_cls
from .patran_neutral import patran_neutral as patran_neutral_cls
from .patran_nodal import patran_nodal as patran_nodal_cls
from .tecplot import tecplot as tecplot_cls
class export(Group):
    """
    Enter the export menu.
    """

    fluent_name = "export"

    child_names = \
        ['sc_def_file_settings', 'settings']

    command_names = \
        ['abaqus', 'mechanical_apdl', 'mechanical_apdl_input', 'ascii', 'avs',
         'ensight', 'ensight_gold', 'fieldview', 'fieldview_data', 'gambit',
         'cgns', 'custom_heat_flux', 'dx', 'ensight_gold_parallel_surfaces',
         'ensight_gold_parallel_volume', 'icemcfd_for_icepak', 'fast_mesh',
         'fast_solution', 'fast_velocity', 'taitherm', 'fieldview_unstruct',
         'fieldview_unstruct_mesh', 'fieldview_unstruct_data',
         'fieldview_unstruct_surfaces', 'ideas', 'nastran', 'patran_neutral',
         'patran_nodal', 'tecplot']

    _child_classes = dict(
        sc_def_file_settings=sc_def_file_settings_cls,
        settings=settings_cls,
        abaqus=abaqus_cls,
        mechanical_apdl=mechanical_apdl_cls,
        mechanical_apdl_input=mechanical_apdl_input_cls,
        ascii=ascii_cls,
        avs=avs_cls,
        ensight=ensight_cls,
        ensight_gold=ensight_gold_cls,
        fieldview=fieldview_cls,
        fieldview_data=fieldview_data_cls,
        gambit=gambit_cls,
        cgns=cgns_cls,
        custom_heat_flux=custom_heat_flux_cls,
        dx=dx_cls,
        ensight_gold_parallel_surfaces=ensight_gold_parallel_surfaces_cls,
        ensight_gold_parallel_volume=ensight_gold_parallel_volume_cls,
        icemcfd_for_icepak=icemcfd_for_icepak_cls,
        fast_mesh=fast_mesh_cls,
        fast_solution=fast_solution_cls,
        fast_velocity=fast_velocity_cls,
        taitherm=taitherm_cls,
        fieldview_unstruct=fieldview_unstruct_cls,
        fieldview_unstruct_mesh=fieldview_unstruct_mesh_cls,
        fieldview_unstruct_data=fieldview_unstruct_data_cls,
        fieldview_unstruct_surfaces=fieldview_unstruct_surfaces_cls,
        ideas=ideas_cls,
        nastran=nastran_cls,
        patran_neutral=patran_neutral_cls,
        patran_nodal=patran_nodal_cls,
        tecplot=tecplot_cls,
    )

