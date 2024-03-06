#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class display_states:
    fluent_name = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : typing.List[str]
                Select objects to be deleted.
        
        """

    def list(self, ):
        """
        'list' command.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

    def use_active(self, state_name: str):
        """
        'use_active' command.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def restore_state(self, state_name: str):
        """
        Apply a display state to the active window.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def copy(self, state_name: str):
        """
        Create a new display state with settings copied from an existing display state.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def read(self, file_name: str):
        """
        Read display states from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_name: str, state_name: List[str]):
        """
        Write display states to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            state_name : typing.List[str]
                'state_name' child.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
