#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class interface:
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

    def rename(self, new: str, old: str):
        """
        Rename the object.
        
        Parameters
        ----------
            new : str
                New name for the object.
            old : str
                Select object to rename.
        
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

    def create(self, name: str, zone1: str, zone2: str, zone1_list: List[str], zone2_list: List[str], mapped: bool, enable_local_mapped_tolerance: bool, use_local_edge_length_factor: bool, local_relative_mapped_tolerance: Union[float, str], local_absolute_mapped_tolerance: Union[float, str], periodic: bool, turbo: bool, turbo_choice: str, mixing_plane: bool, turbo_non_overlap: bool, coupled: bool, matching: bool, static: bool):
        """
        Create mesh interfaces.
        
        Parameters
        ----------
            name : str
                Enter a prefix for mesh interface names.
            zone1 : str
                Select first interface zones for pairing.
            zone2 : str
                Select second interface zones for pairing.
            zone1_list : typing.List[str]
                Select first interface defining this mesh-interface.
            zone2_list : typing.List[str]
                Select second interface defining this mesh-interface.
            mapped : bool
                Indicate if mesh-interface is mapped.
            enable_local_mapped_tolerance : bool
                Enable local tolerance for this mesh interface.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            local_relative_mapped_tolerance : real
                Tolerance.
            local_absolute_mapped_tolerance : real
                Tolerance.
            periodic : bool
                Indicate if mesh-interface is adjacent to periodic boundaries.
            turbo : bool
                Create a general turbo interface.
            turbo_choice : str
                Enter your choice of pitch-change types.
            mixing_plane : bool
                If you want to use mixing plane mechanism.
            turbo_non_overlap : bool
                Create non-overlapping walls for gti interfaces.
            coupled : bool
                Indicate if mesh-interface is coupled.
            matching : bool
                Indicate if mesh-interface is matching.
            static : bool
                Indicate if mesh-interface is static.
        
        """

    <class 'ansys.fluent.core.solver.flobject.child_object_type'> = ...
