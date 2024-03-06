#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class system_coupling:
    fluent_name = ...
    child_names = ...
    htc = ...
    unsteady_statistics = ...
    user_defined_coupling_variables_via_udm = ...
    use_face_or_element_based_data_transfer = ...
    command_names = ...

    def write_scp_file(self, file_name: str):
        """
        Write fluent input scp file for sc.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def connect_parallel(self, schost: str, scport: int, scname: str):
        """
        System coupling connection status.
        
        Parameters
        ----------
            schost : str
                Sc solver host input.
            scport : int
                Sc solver port input.
            scname : str
                Sc solver name input.
        
        """

    def init_and_solve(self, ):
        """
        System-coupling-solve-init-command.
        """

    def solve(self, ):
        """
        System-coupling-solve-command.
        """

