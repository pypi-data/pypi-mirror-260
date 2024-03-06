#
# This is an auto-generated file.  DO NOT EDIT!
#


from typing import Union, List, Tuple

class scene_animation:
    fluent_name = ...
    child_names = ...
    set_custom_frames = ...
    command_names = ...

    def read_animation(self, file_name: str):
        """
        'read_animation' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write_animation(self, format_name: str, file_name: str):
        """
        Write keyframe Animation file.
        
        Parameters
        ----------
            format_name : str
                'format_name' child.
            file_name : str
                'file_name' child.
        
        """

    def add_keyframe(self, key: int):
        """
        Add keyframe.
        
        Parameters
        ----------
            key : int
                'key' child.
        
        """

    def delete_keyframe(self, key: int):
        """
        Delete a keyframe.
        
        Parameters
        ----------
            key : int
                'key' child.
        
        """

    def delete_all_keyframes(self, ):
        """
        Delete all keyframes.
        """

    def play(self, start_keyframe: int, end_keyframe: int, increment: int):
        """
        Play keyframe animation.
        
        Parameters
        ----------
            start_keyframe : int
                Set start keyframe.
            end_keyframe : int
                Set end keyframe.
            increment : int
                Set increment.
        
        """

