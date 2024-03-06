#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class conductive_regions:
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        List properties of selected object.
        
        Parameters
        ----------
            object_at : int
                Select object index to delete.
        
        """

    def add_zone(self, zone_name: str, value: Union[float, str]):
        """
        'add_zone' command.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            value : real
                'value' child.
        
        """

    def list_zone(self, ):
        """
        'list_zone' command.
        """

    def delete_zone(self, face_name: str):
        """
        'delete_zone' command.
        
        Parameters
        ----------
            face_name : str
                Pick ~a zone you want to delete.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
