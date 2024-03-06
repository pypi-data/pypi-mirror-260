#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class case_modification:
    fluent_name = ...
    child_names = ...
    enabled = ...
    initialization_method = ...
    case_modification = ...
    command_names = ...

    def automatic_initialization(self, initialization_type: str, data_file_name: str, init_from_solution: str, data_file_name2: str):
        """
        Define how the case is to be initialized automatically.
        
        Parameters
        ----------
            initialization_type : str
                'initialization_type' child.
            data_file_name : str
                'data_file_name' child.
            init_from_solution : str
                'init_from_solution' child.
            data_file_name2 : str
                'data_file_name2' child.
        
        """

    def execute_strategy(self, save_mode: str, continue_with_current_mesh: bool, discard_all_data: bool):
        """
        Execute the automatic initialization and case modification strategy defined at present .
        
        Parameters
        ----------
            save_mode : str
                'save_mode' child.
            continue_with_current_mesh : bool
                Reloading of the upstream mesh data is desired. Is it needed to continue with currently loaded mesh?.
            discard_all_data : bool
                'discard_all_data' child.
        
        """

    def enable_strategy(self, enable: bool):
        """
        Specify whether automatic initialization and case modification should be enabled.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        
        """

    def copy_modification(self, mod_name: str):
        """
        Copy a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def delete_modification(self, mod_name: str):
        """
        Delete a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def enable_modification(self, mod_name: str):
        """
        Enable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def disable_modification(self, mod_name: str):
        """
        Disable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        
        """

    def import_modifications(self, filename: str):
        """
        Import a list of case modifications from a tsv file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def export_modifications(self, command_list: List[str], filename: str):
        """
        Export all case modifications to a tsv file.
        
        Parameters
        ----------
            command_list : typing.List[str]
                'command_list' child.
            filename : str
                'filename' child.
        
        """

    def continue_strategy_execution(self, ):
        """
        Continue execution of the automatic initialization and case modification strategy defined at present.
        """

