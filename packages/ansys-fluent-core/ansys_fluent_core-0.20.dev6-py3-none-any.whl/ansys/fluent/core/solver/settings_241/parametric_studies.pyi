#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class parametric_studies:
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
        List the names of the objects.
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

    def initialize(self, project_filename: str):
        """
        Start Parametric Study.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        
        """

    def duplicate(self, copy_design_points: bool):
        """
        Duplicate Parametric Study.
        
        Parameters
        ----------
            copy_design_points : bool
                'copy_design_points' child.
        
        """

    def set_as_current(self, study_name: str):
        """
        Set As Current Study.
        
        Parameters
        ----------
            study_name : str
                'study_name' child.
        
        """

    def use_base_data(self, ):
        """
        Use Base Data.
        """

    def export_design_table(self, filepath: str):
        """
        Export Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
        
        """

    def import_design_table(self, filepath: str, delete_existing: bool):
        """
        Import Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
            delete_existing : bool
                'delete_existing' child.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
