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

    def resize(self, size: int):
        """
        Set number of objects for list-object.
        
        Parameters
        ----------
            size : int
                New size for list-object.
        
        """

    def add_zone(self, zone_name: str, value: Union[float, str]):
        """
        Add thread-real-pair object.
        
        Parameters
        ----------
            zone_name : str
                Specify zone name in add-zone operation.
            value : real
                Specify value in add-zone operation.
        
        """

    def list_zone(self, ):
        """
        List thread-real-pair object.
        """

    def delete_zone(self, face_name: str):
        """
        Delete thread-real-pair object.
        
        Parameters
        ----------
            face_name : str
                Pick a zone you want to delete.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
