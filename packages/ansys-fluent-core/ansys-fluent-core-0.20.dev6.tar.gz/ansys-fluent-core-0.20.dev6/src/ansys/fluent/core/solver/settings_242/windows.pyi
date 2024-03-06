#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class windows:
    fluent_name = ...
    child_names = ...
    axes = ...
    main = ...
    scale = ...
    text = ...
    video = ...
    xy = ...
    logo = ...
    ruler = ...
    logo_color = ...
    command_names = ...

    def aspect_ratio(self, width: Union[float, str], height: Union[float, str]):
        """
        Set the aspect ratio of the active window.
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        
        """

    def open_window(self, window_id: int):
        """
        Open a user graphics window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def set_window(self, window_id: int):
        """
        Set a user graphics window to be the active window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def set_window_by_name(self, window_name: str):
        """
        Set a reserved graphics window to be the active window by its name.
        
        Parameters
        ----------
            window_name : str
                'window_name' child.
        
        """

    def close_window(self, window_id: int):
        """
        Close a user graphics window.
        
        Parameters
        ----------
            window_id : int
                'window_id' child.
        
        """

    def close_window_by_name(self, window_name: str):
        """
        Close a reserved graphics window by its name.
        
        Parameters
        ----------
            window_name : str
                'window_name' child.
        
        """

