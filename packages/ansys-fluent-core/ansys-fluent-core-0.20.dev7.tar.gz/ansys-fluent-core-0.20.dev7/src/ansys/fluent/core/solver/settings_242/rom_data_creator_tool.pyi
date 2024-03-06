#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class rom_data_creator_tool:
    fluent_name = ...
    child_names = ...
    rom_type = ...
    transient_setup = ...
    file_saving_frequency = ...
    joule_heat_parameter = ...
    command_names = ...

    def add_rom_parameter(self, parameter_type: str, entity_list: List[str], group_value: Union[float, str], individual_or_group: bool, individual_value: bool, value_list: List[Union[float, str]]):
        """
        Add parameter command.
        
        Parameters
        ----------
            parameter_type : str
                Set parameter type.
            entity_list : typing.List[str]
                Entity list name.
            group_value : real
                Set group value.
            individual_or_group : bool
                Set as-group option.
            individual_value : bool
                Set individual value for different entities in the group.
            value_list : typing.List[real]
                Set values for the different entities in the group.
        
        """

    def rom_data_creator(self, rom_type: int):
        """
        ROM data creator.
        
        Parameters
        ----------
            rom_type : int
                ROM type in ROM-data creator.
        
        """

    def create_journal_file(self, rom_type: int):
        """
        Create journal file.
        
        Parameters
        ----------
            rom_type : int
                ROM type in the ROM simulation.
        
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

