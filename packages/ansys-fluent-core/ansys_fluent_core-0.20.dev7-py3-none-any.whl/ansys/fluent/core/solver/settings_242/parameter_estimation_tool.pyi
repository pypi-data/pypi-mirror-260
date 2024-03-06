#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class parameter_estimation_tool:
    fluent_name = ...
    child_names = ...
    echem_model = ...
    thermal_abuse_fitting = ...
    command_names = ...

    def ntgk_curve_fitting(self, filename: List[str], capacity: Union[float, str], number_dod_level: int, min_dod: Union[float, str], max_dod: Union[float, str], capacity_fade_enabled: bool):
        """
        NTGK parameter estimation tool.
        
        Parameters
        ----------
            filename : typing.List[str]
                File names used in the NTGK model fitting.
            capacity : real
                Battery capacity used in the NTGK model fitting.
            number_dod_level : int
                Number of DOD-levels used in the NTGK model fitting.
            min_dod : real
                Minimum DOD used in the NTGK model fitting.
            max_dod : real
                Maximum DOD used in the NTGK model fitting.
            capacity_fade_enabled : bool
                Include Capacity Fade Effect in the NTGK model fitting.
        
        """

    def ecm_curve_fitting(self, filename: List[str], capacity: Union[float, str], circuit_model: str, fitting_method: str, rs_fix: List[Union[float, str]], capacity_fade_enabled: bool, read_discharge_file_enabled: bool, number_discharge_file: int, discharge_filename: List[str]):
        """
        ECM parameter estimation tool.
        
        Parameters
        ----------
            filename : typing.List[str]
                File names used in ECM model parameter fitting.
            capacity : real
                Battery capacity used in ECM model parameter fitting.
            circuit_model : str
                Circuit model used in ECM model parameter fitting.
            fitting_method : str
                Fitting method used in ECM model parameter fitting.
            rs_fix : typing.List[real]
                Fix-Rs used in ECM model parameter fitting.
            capacity_fade_enabled : bool
                Include capacity fade effect used in ECM model parameter fitting.
            read_discharge_file_enabled : bool
                Import discharging curves used in ECM model parameter fitting.
            number_discharge_file : int
                Number of total discharging files used in ECM model parameter fitting.
            discharge_filename : typing.List[str]
                File name for discharing curve used in ECM model parameter fitting.
        
        """

