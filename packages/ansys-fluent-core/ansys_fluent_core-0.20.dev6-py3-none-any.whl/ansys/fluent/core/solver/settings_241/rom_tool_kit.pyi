#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class rom_tool_kit:
    fluent_name = ...
    child_names = ...
    rom_type = ...
    joule_heat_parameter = ...
    transient_setup = ...
    file_saving_frequency = ...
    lti_rom_generation = ...
    command_names = ...

    def add_rom_parameter(self, parameter_type: int, entity_list: List[str], individual_or_group: bool, individual_value: bool, group_value: Union[float, str], value_list: List[Union[float, str]]):
        """
        'add_rom_parameter' command.
        
        Parameters
        ----------
            parameter_type : int
                'parameter_type' child.
            entity_list : typing.List[str]
                'entity_list' child.
            individual_or_group : bool
                'individual_or_group' child.
            individual_value : bool
                'individual_value' child.
            group_value : real
                'group_value' child.
            value_list : typing.List[real]
                'value_list' child.
        
        """

    def rom_data_creator(self, ):
        """
        Non-conformal Interface Matching.
        """

    def list_rom_parameter(self, ):
        """
        Print all ROM-related paramters.
        """

    def delete_rom_parameter(self, parameter_names: List[str]):
        """
        Delete ROM-related paramters.
        
        Parameters
        ----------
            parameter_names : typing.List[str]
                Set deleted parameter lists.
        
        """

