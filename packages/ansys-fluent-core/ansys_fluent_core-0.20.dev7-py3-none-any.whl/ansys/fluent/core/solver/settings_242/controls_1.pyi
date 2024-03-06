#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class controls:
    fluent_name = ...
    child_names = ...
    courant_number = ...
    p_v_controls = ...
    relaxation_factor = ...
    under_relaxation = ...
    pseudo_time_method_local_time_step = ...
    pseudo_time_explicit_relaxation_factor = ...
    acoustics_wave_eqn_controls = ...
    contact_solution_controls = ...
    equations = ...
    limits = ...
    advanced = ...
    command_names = ...

    def reset_solution_controls(self, ):
        """
        Reset the solution controls to default.
        """

    def reset_amg_controls(self, ):
        """
        Rest AMG controls to default.
        """

    def reset_multi_stage_parameters(self, ):
        """
        Reset multi-stage parameters.
        """

    def reset_limits(self, ):
        """
        Reset limits to default.
        """

    def reset_pseudo_time_method_generic(self, ):
        """
        Set pseudo time method parameters to default.
        """

    def reset_pseudo_time_method_equations(self, ):
        """
        Set pseudo time method equation specific usage to default.
        """

    def reset_pseudo_time_method_relaxations(self, ):
        """
        Set pseudo time method relaxation factors to default.
        """

    def reset_pseudo_time_method_scale_factors(self, ):
        """
        Set pseudo time method time scale factors to default.
        """

