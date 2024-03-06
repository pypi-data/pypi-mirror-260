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

from .a_sei import a_sei as a_sei_cls
from .e_sei import e_sei as e_sei_cls
from .m_sei import m_sei as m_sei_cls
from .h_sei import h_sei as h_sei_cls
from .w_sei import w_sei as w_sei_cls
from .sei0 import sei0 as sei0_cls
from .a_ne import a_ne as a_ne_cls
from .e_ne import e_ne as e_ne_cls
from .m_ne import m_ne as m_ne_cls
from .h_ne import h_ne as h_ne_cls
from .w_ne import w_ne as w_ne_cls
from .ne0 import ne0 as ne0_cls
from .ne_tsei_ref import ne_tsei_ref as ne_tsei_ref_cls
from .ne_tsei0 import ne_tsei0 as ne_tsei0_cls
from .a_pe import a_pe as a_pe_cls
from .e_pe import e_pe as e_pe_cls
from .m1_pe import m1_pe as m1_pe_cls
from .m2_pe import m2_pe as m2_pe_cls
from .h_pe import h_pe as h_pe_cls
from .w_pe import w_pe as w_pe_cls
from .pe0 import pe0 as pe0_cls
from .a_e import a_e as a_e_cls
from .e_e import e_e as e_e_cls
from .m_e import m_e as m_e_cls
from .h_e import h_e as h_e_cls
from .w_e import w_e as w_e_cls
from .e0 import e0 as e0_cls
class four_equation(Group):
    """
    'four_equation' child.
    """

    fluent_name = "four-equation"

    child_names = \
        ['a_sei', 'e_sei', 'm_sei', 'h_sei', 'w_sei', 'sei0', 'a_ne', 'e_ne',
         'm_ne', 'h_ne', 'w_ne', 'ne0', 'ne_tsei_ref', 'ne_tsei0', 'a_pe',
         'e_pe', 'm1_pe', 'm2_pe', 'h_pe', 'w_pe', 'pe0', 'a_e', 'e_e', 'm_e',
         'h_e', 'w_e', 'e0']

    _child_classes = dict(
        a_sei=a_sei_cls,
        e_sei=e_sei_cls,
        m_sei=m_sei_cls,
        h_sei=h_sei_cls,
        w_sei=w_sei_cls,
        sei0=sei0_cls,
        a_ne=a_ne_cls,
        e_ne=e_ne_cls,
        m_ne=m_ne_cls,
        h_ne=h_ne_cls,
        w_ne=w_ne_cls,
        ne0=ne0_cls,
        ne_tsei_ref=ne_tsei_ref_cls,
        ne_tsei0=ne_tsei0_cls,
        a_pe=a_pe_cls,
        e_pe=e_pe_cls,
        m1_pe=m1_pe_cls,
        m2_pe=m2_pe_cls,
        h_pe=h_pe_cls,
        w_pe=w_pe_cls,
        pe0=pe0_cls,
        a_e=a_e_cls,
        e_e=e_e_cls,
        m_e=m_e_cls,
        h_e=h_e_cls,
        w_e=w_e_cls,
        e0=e0_cls,
    )

