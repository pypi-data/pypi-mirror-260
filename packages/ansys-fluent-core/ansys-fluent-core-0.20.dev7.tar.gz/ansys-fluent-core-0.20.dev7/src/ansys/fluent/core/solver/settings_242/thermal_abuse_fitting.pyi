#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class thermal_abuse_fitting:
    fluent_name = ...
    child_names = ...
    test_data_sets = ...
    rhocp = ...
    area = ...
    vol = ...
    epsilon = ...
    fixm_enabled = ...
    mvalue = ...
    fixn_enabled = ...
    nvalue = ...
    filename = ...
    initial_temp = ...
    ambient_temp = ...
    external_ht_coeff = ...
    enclosure_temp = ...
    command_names = ...

    def abuse_curve_fitting(self, ):
        """
        Thermal abuse curve fitting.
        """

    def fine_tune_parameter(self, user_a: Union[float, str], user_e: Union[float, str], user_m: Union[float, str], user_n: Union[float, str]):
        """
        Fine tune Arrhenius rate parameters.
        
        Parameters
        ----------
            user_a : real
                Specify fine-tuning parameter A in abuse model fitting.
            user_e : real
                Specify fine-tuning parameter E in abuse model fitting.
            user_m : real
                Specify fine-tuning parameter m in abuse model fitting.
            user_n : real
                Specify fine-tuning parameter n in abuse model fitting.
        
        """

    def use_fine_tune_parameter(self, apply: bool):
        """
        Command to use fine-tuned parameters.
        
        Parameters
        ----------
            apply : bool
                Use fine-tuned parameters.
        
        """

