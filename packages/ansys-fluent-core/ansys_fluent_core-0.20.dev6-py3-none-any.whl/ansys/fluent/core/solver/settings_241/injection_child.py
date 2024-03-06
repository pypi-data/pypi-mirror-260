#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .injection_thread import injection_thread as injection_thread_cls
from .coupled import coupled as coupled_cls
from .extraction_thread import extraction_thread as extraction_thread_cls
from .uniform import uniform as uniform_cls
from .injection_hole_count import injection_hole_count as injection_hole_count_cls
from .discrete_ext import discrete_ext as discrete_ext_cls
from .static import static as static_cls
from .formulation import formulation as formulation_cls
from .holes_setup import holes_setup as holes_setup_cls
from .dynamic_setup import dynamic_setup as dynamic_setup_cls
from .static_setup import static_setup as static_setup_cls
class injection_child(Group):
    """
    'child_object_type' of injection.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['injection_thread', 'coupled', 'extraction_thread', 'uniform',
         'injection_hole_count', 'discrete_ext', 'static', 'formulation',
         'holes_setup', 'dynamic_setup', 'static_setup']

    _child_classes = dict(
        injection_thread=injection_thread_cls,
        coupled=coupled_cls,
        extraction_thread=extraction_thread_cls,
        uniform=uniform_cls,
        injection_hole_count=injection_hole_count_cls,
        discrete_ext=discrete_ext_cls,
        static=static_cls,
        formulation=formulation_cls,
        holes_setup=holes_setup_cls,
        dynamic_setup=dynamic_setup_cls,
        static_setup=static_setup_cls,
    )

