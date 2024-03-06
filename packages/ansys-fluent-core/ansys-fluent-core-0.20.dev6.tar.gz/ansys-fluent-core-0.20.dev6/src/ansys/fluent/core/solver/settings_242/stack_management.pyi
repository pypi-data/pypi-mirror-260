#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class stack_management:
    fluent_name = ...
    command_names = ...

    def list_fc_units(self, ):
        """
        List fuel cell units.
        """

    def stack_create_fcu(self, fcu_name: str, cellzones: List[str]):
        """
        Create stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
            cellzones : typing.List[str]
                Enter cell zone name list.
        
        """

    def stack_modify_fcu(self, fcu_name: str, cellzones: List[str]):
        """
        Modify stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
            cellzones : typing.List[str]
                Enter cell zone name list.
        
        """

    def stack_delete_fcu(self, fcu_name: str):
        """
        Delete stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
        
        """

    def stack_reset_fcu(self, reset: bool):
        """
        Reset stack units.
        
        Parameters
        ----------
            reset : bool
                'reset' child.
        
        """

    def stack_submit_fcu(self, submit: bool):
        """
        Apply stack units settings.
        
        Parameters
        ----------
            submit : bool
                'submit' child.
        
        """

