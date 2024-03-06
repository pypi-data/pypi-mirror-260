#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class modify_zones:
    fluent_name = ...
    command_names = ...

    def deactivate_cell_zone(self, cell_deactivate_list: List[str]):
        """
        Deactivate cell thread.
        
        Parameters
        ----------
            cell_deactivate_list : typing.List[str]
                Deactivate a cell zone.
        
        """

    def delete_cell_zone(self, cell_zones: List[str]):
        """
        Delete a cell thread.
        
        Parameters
        ----------
            cell_zones : typing.List[str]
                Delete a cell zone.
        
        """

    def copy_move_cell_zone(self, cell_zone_name: str, translate: bool, rotation_angle: Union[float, str], offset: List[Union[float, str]], axis: List[Union[float, str]]):
        """
        Copy and translate or rotate a cell zone.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a cell zone name.
            translate : bool
                Specify if copied zone should be translated (#t) or rotated (#f).
            rotation_angle : real
                'rotation_angle' child.
            offset : typing.List[real]
                'offset' child.
            axis : typing.List[real]
                'axis' child.
        
        """

    def list_zones(self, ):
        """
        List zone IDs, types, kinds, and names.
        """

    def extrude_face_zone_delta(self, face_zone: str, distance_delta: List[Union[float, str]]):
        """
        Extrude a face thread a specified distance based on a list of deltas.
        
        Parameters
        ----------
            face_zone : str
                Enter a zone name.
            distance_delta : typing.List[real]
                'distance_delta' child.
        
        """

    def extrude_face_zone_para(self, face_zone: str, normal_distance: Union[float, str], parametric_coordinates: List[Union[float, str]]):
        """
        Extrude a face thread a specified distance based on a distance and a list of parametric locations between 0 and 1 (eg. 0 0.2 0.4 0.8 1.0).
        
        Parameters
        ----------
            face_zone : str
                Enter a zone name.
            normal_distance : real
                'normal_distance' child.
            parametric_coordinates : typing.List[real]
                'parametric_coordinates' child.
        
        """

    def fuse_face_zones(self, zone_names: List[str], zone_name: str):
        """
        Attempt to fuse zones by removing duplicate faces and nodes.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Merge duplicate faces and nodes of zones in list.
            zone_name : str
                'zone_name' child.
        
        """

    def scale_zone(self, zone_names: List[str], scale: List[Union[float, str]]):
        """
        Scale nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Scale specified cell zones.
            scale : typing.List[real]
                'scale' child.
        
        """

    def rotate_zone(self, zone_names: List[str], rotation_angle: Union[float, str], origin: List[Union[float, str]], axis: List[Union[float, str]]):
        """
        Rotate nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Rotate specified cell zones.
            rotation_angle : real
                'rotation_angle' child.
            origin : typing.List[real]
                'origin' child.
            axis : typing.List[real]
                'axis' child.
        
        """

    def translate_zone(self, zone_names: List[str], offset: List[Union[float, str]]):
        """
        Translate nodal coordinates of input cell zones.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Translate specified cell zones.
            offset : typing.List[real]
                'offset' child.
        
        """

    def merge_zones(self, zone_names: List[str]):
        """
        Merge zones of the same type and condition into one.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone name list.
        
        """

    def replace_zone(self, file_name: str, zone_1_name: str, zone_2_name: str, interpolate: bool):
        """
        Replace a cell zone.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            zone_1_name : str
                Enter a zone name.
            zone_2_name : str
                'zone_2_name' child.
            interpolate : bool
                'interpolate' child.
        
        """

    def append_mesh(self, file_name: str):
        """
        Append new mesh.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def append_mesh_data(self, file_name: str):
        """
        Append new mesh with data.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def sep_cell_zone_mark(self, cell_zone_name: str, register: str, move_faces: bool):
        """
        Separate a cell zone based on cell marking.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a zone name.
            register : str
                'register' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_cell_zone_region(self, cell_zone_name: str, move_cells: bool):
        """
        Separate a cell zone based on contiguous regions.
        
        Parameters
        ----------
            cell_zone_name : str
                Enter a zone name.
            move_cells : bool
                'move_cells' child.
        
        """

    def sep_face_zone_angle(self, face_zone_name: str, angle: Union[float, str], move_faces: bool):
        """
        Separate a face zone based on significant angle.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            angle : real
                'angle' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_face(self, face_zone_name: str, move_faces: bool):
        """
        Separate each face in a zone into unique zone.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_mark(self, face_zone_name: str, register_name: str, move_faces: bool):
        """
        Separate a face zone based on cell marking.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            register_name : str
                'register_name' child.
            move_faces : bool
                'move_faces' child.
        
        """

    def sep_face_zone_region(self, face_zone_name: str, move_faces: bool):
        """
        Separate a face zone based on contiguous regions.
        
        Parameters
        ----------
            face_zone_name : str
                Enter a zone name.
            move_faces : bool
                'move_faces' child.
        
        """

    def zone_name(self, zone_name: str, new_name: str):
        """
        Give a zone a new name.
        
        Parameters
        ----------
            zone_name : str
                Enter a zone name.
            new_name : str
                'new_name' child.
        
        """

    def change_zone_state(self, zone_name: str, domain: str, new_phase: int):
        """
        Change the realgas material state for a zone.
        
        Parameters
        ----------
            zone_name : str
                Enter a fluid zone name.
            domain : str
                'domain' child.
            new_phase : int
                'new_phase' child.
        
        """

    def make_periodic(self, zone_name: str, shadow_zone_name: str, rotate_periodic: bool, create: bool, auto_translation: bool, direction: List[Union[float, str]]):
        """
        Attempt to establish conformal periodic face zone connectivity.
        
        Parameters
        ----------
            zone_name : str
                Enter id/name of zone to convert to periodic.
            shadow_zone_name : str
                Enter id/name of zone to convert to shadow.
            rotate_periodic : bool
                'rotate_periodic' child.
            create : bool
                'create' child.
            auto_translation : bool
                'auto_translation' child.
            direction : typing.List[real]
                'direction' child.
        
        """

    def create_periodic_interface(self, periodic_method: str, interface_name: str, zone_name: str, shadow_zone_name: str, rotate_periodic: bool, new_axis: bool, origin: List[Union[float, str]], new_direction: bool, direction: List[Union[float, str]], auto_angle: bool, rotation_angle: Union[float, str], auto_translation: bool, translation: List[Union[float, str]], create_periodic: bool, auto_offset: bool, nonconformal_angle: Union[float, str], nonconformal_translation: List[Union[float, str]], create_matching: bool, nonconformal_create_periodic: bool):
        """
        Create a conformal or non-conformal periodic interface.
        
        Parameters
        ----------
            periodic_method : str
                Enter method.
            interface_name : str
                Enter a name for this periodic interface.
            zone_name : str
                Enter id/name of zone to convert to periodic.
            shadow_zone_name : str
                Enter id/name of zone to convert to shadow.
            rotate_periodic : bool
                'rotate_periodic' child.
            new_axis : bool
                'new_axis' child.
            origin : typing.List[real]
                'origin' child.
            new_direction : bool
                'new_direction' child.
            direction : typing.List[real]
                'direction' child.
            auto_angle : bool
                'auto_angle' child.
            rotation_angle : real
                'rotation_angle' child.
            auto_translation : bool
                'auto_translation' child.
            translation : typing.List[real]
                'translation' child.
            create_periodic : bool
                'create_periodic' child.
            auto_offset : bool
                'auto_offset' child.
            nonconformal_angle : real
                'nonconformal_angle' child.
            nonconformal_translation : typing.List[real]
                'nonconformal_translation' child.
            create_matching : bool
                'create_matching' child.
            nonconformal_create_periodic : bool
                'nonconformal_create_periodic' child.
        
        """

    def slit_periodic(self, periodic_zone_name: str, slit_periodic: bool):
        """
        Slit a periodic zone into two symmetry zones.
        
        Parameters
        ----------
            periodic_zone_name : str
                Enter id/name of periodic zone to slit.
            slit_periodic : bool
                'slit_periodic' child.
        
        """

    def zone_type(self, zone_names: List[str], new_type: str):
        """
        Set a zone's type.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Enter zone id/name.
            new_type : str
                'new_type' child.
        
        """

