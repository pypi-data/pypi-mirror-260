#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class surface_integrals:
    fluent_name = ...
    command_names = ...

    def area(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total area of surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def area_weighted_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print area-weighted average of scalar on surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_based_flux(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector based flux.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_flux(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector flux.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_weighted_average(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector weighted average.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print average of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_min(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_max(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print flow rate of scalar through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def integral(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print integral of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass_flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass flow rate through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass_weighted_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-average of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def standard_deviation(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print standard deviation of scalar.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def sum(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def uniformity_index_area_weighted(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print uniformity index of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def uniformity_index_mass_weighted(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print uniformity index of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print average of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_min(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_max(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximkum of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def volume_flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume flow rate through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

