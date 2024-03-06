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

from .use_sided_area_vector import use_sided_area_vector as use_sided_area_vector_cls
from .use_nci_sided_area_vectors import use_nci_sided_area_vectors as use_nci_sided_area_vectors_cls
from .recreate import recreate as recreate_cls
class change_numerics(Command):
    """
    Enable modified non-conformal interface numerics.
    
    Parameters
    ----------
        use_sided_area_vector : bool
            'use_sided_area_vector' child.
        use_nci_sided_area_vectors : bool
            'use_nci_sided_area_vectors' child.
        recreate : bool
            'recreate' child.
    
    """

    fluent_name = "change-numerics?"

    argument_names = \
        ['use_sided_area_vector', 'use_nci_sided_area_vectors', 'recreate']

    _child_classes = dict(
        use_sided_area_vector=use_sided_area_vector_cls,
        use_nci_sided_area_vectors=use_nci_sided_area_vectors_cls,
        recreate=recreate_cls,
    )

