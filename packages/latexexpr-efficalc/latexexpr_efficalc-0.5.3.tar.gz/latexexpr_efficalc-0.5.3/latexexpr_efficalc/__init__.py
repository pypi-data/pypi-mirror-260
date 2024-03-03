# coding=utf8
# -*- coding: utf8 -*-
#
#      LaTeX Expression : Python module for easy LaTeX typesetting of algebraic
#  expressions in symbolic form with automatic substitution and result computation
#
#                       Copyright (C)  2013-2015  Jan Stransky
#                       Copyright (C)  2022  	  Jakub Kaderka
#                       Copyright (C)  2024  	  Andrew Young
#
#  LaTeX Expression is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  LaTeX Expression is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
#  details.
#
#  You should have received a copy of the GNU Lesser General Public License along
#  with this program. If not, see <http://www.gnu.org/licenses/>.

r"""
LaTeX Expression is a Python module for easy LaTeX typesetting of algebraic expressions in symbolic form with automatic substitution and result computation,
i.e. of the form var = generalExpression = substitutedExpression = result, e.g.

.. code-block:: none

	r = 3.0 m
	F = 4.0 kN
	M = r*F = 3.0*4.0 = 12 kNm

The expression is based on :class:`.Variable` class, representing physical or mathematical variable (with symbolic name, value and unit). :class:`Expression` has similar meaning, except that instead of value it contains its :class:`Operation`. :class:`Operation` contains its type (all basic operations are implemented, see :ref:`predefinedOperations`) and combine one or more :class:`variable(s) <.Variable>`, :class:`expression(s) <.Expression>` or other :class:`operations <.Operation>`. In this way, the hierarchy of operations may be combined in one :class:`Expression`. Furthermore, where it is reasonable, Python operators are overloaded to make things even more simple and clear.

.. code-block:: python

	>>> v1 = Variable('a_{22}',3.45,'mm')
	>>> print v1
	a_{22} = 3.45 \ \mathrm{mm}
	>>> v2 = Variable('F',5.876934835,'kN')
	>>> print v2
	F = 5.87693 \ \mathrm{kN}
	>>> v3 = Variable('F',4.34,'kN',exponent=-2)
	>>> print v3
	F = { 434 \cdot 10^{-2} } \ \mathrm{kN}
	>>> v4 = Variable('F',2.564345,'kN',format='%.4f')
	>>> print v4
	F = 2.5643 \ \mathrm{kN}
	>>> v5 = Variable('F',5.876934835,'kN')
	>>> print v5
	F = 5.87693 \ \mathrm{kN}
	>>> v6 = Variable('F',-6.543,'kN')
	>>> o1 = (v1 + sqrt(v2)) / (v3 * v4) + v5
	>>> print o1
	\frac{ {a_{22}} + \sqrt{ {F} } }{ {F} \cdot {F} } + {F} = \frac{ 3.45 + \sqrt{ 5.87693 } }{ { 434 \cdot 10^{-2} } \cdot 2.5643 } + 5.87693
	>>> e1 = Expression('E_1^i',s_brackets(o1) - sqr(v6),'kNm')
	>>> print e1
	E_1^i = \left[ \frac{ {a_{22}} + \sqrt{ {F} } }{ {F} \cdot {F} } + {F} \right] - {F}^2 = \left[ \frac{ 3.45 + \sqrt{ 5.87693 } }{ { 434 \cdot 10^{-2} } \cdot 2.5643 } + 5.87693 \right] - \left( -6.543 \right)^2 = \left(-36.4061\right) \ \mathrm{kNm}
	>>> v7 = e1.to_variable()
	>>> print v7
	E_1^i = \left( -36.4061 \right) \ \mathrm{kNm}
	>>> print v7.to_latex_variable_all('MYV7')
	\def\MYV7{E_1^i = \left( -36.4061 \right) \ \mathrm{kNm}}
	>>> v8 = Variable('F',None,'kN')
	>>> o4 = v1 + v8
	>>> e4 = Expression('E_4',o4,'mF')
	>>> print v8
	F
	>>> print o4
	{a_{22}} + {F}
	>>> print e4
	E_4 = {a_{22}} + {F}
	>>> v8.value=2.34
	>>> print v8
	F = 2.34 \ \mathrm{kN}
	>>> print o4
	{a_{22}} + {F} = 3.45 + 2.34
	>>> print e4
	E_4 = {a_{22}} + {F} = 3.45 + 2.34 = 5.79 \ \mathrm{mF}


The module is distributed under `GNU LGPL license <http://www.gnu.org/licenses/lgpl.html>`_

To see the module "in action", visit `project home page <http://mech.fsv.cvut.cz/~stransky/en/software/latexexpr/>`_.
"""

import math
from functools import reduce

version = "0.4"
date = "2022-05-31"
_DEBUG = False


class LaTeXExpressionError(Exception):
    """Module exception class"""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


# Auxiliary functions
def _add(self, v):
    return add(self, v)


def _sub(self, v):
    return sub(self, v)


def _mul(self, v):
    return mul(self, v)


def _div(self, v):
    return div(self, v)


def _div2(self, v):
    return div2(self, v)


def _pow(self, v):
    return power(self, v)


def _radd(self, v):
    return add(v, self)


def _rsub(self, v):
    return sub(v, self)


def _rmul(self, v):
    return mul(v, self)


def _rtruediv(self, v):
    return div(v, self)


def _rdiv2(self, v):
    return div2(v, self)


def _rpow(self, v):
    return power(v, self)


def _neg(self):
    return neg(self)


def _pos(self):
    return pos(self)


def _abs(self):
    return absolute(self)


######################################################################
# Variable class
######################################################################
class Variable(object):
    r"""Class representing mathematical or physical variable, containing information about its symbolic name, value, phyical units and how to format it. It is a fundamental building block of :class:`operations <.Operation>` and :class:`expressions <.Expression>` instances.

    This class overloads str() method to return expression "name = value unit", float() to return numeric result (throws exception if value is None) and absolute() method.

    This class also overloads +,-,*,/ (division, frac{...}{...} in LaTeX), // (divsion, .../... in LaTeX) and ** (power) operators. They can be used with Variable, Expression or Operation instances resulting into new Operation instance.

    :param str name: symbolic name of the variable
    :param float|str|None value: value of the variable. If value==None, than the Variable is considered as symbolic
    :param str unit: physical unit of the variable
    :param str format: python string to be formatted by the numeric value with '%' operation (e.g. '%e', '%g', '%.4g', '%.3f' etc.). See `Python string formatting docs <http://docs.python.org/2/library/stdtypes.html#string-formatting-operations>`_ for more details.
    :param str unit_format: python string to be formatted with unit (default is '\mathrm{%s}' for non-italic units inside math mode). For no formatting use '%s'. See `Python string formatting docs <http://docs.python.org/2/library/stdtypes.html#string-formatting-operations>`_ for more details.
    :param int exponent: exponent for scientific representation

    .. code-block:: python

            >>> v1 = Variable('a_{22}',3.45,'mm')
            >>> print v1
            a_{22} = 3.45 \ \mathrm{mm}
            >>> v2 = Variable('F',5.876934835,'kN')
            >>> print v2
            F = 5.87693 \ \mathrm{kN}
            >>> v3 = Variable('F',4.34,'kN',exponent=-2)
            >>> print v3
            F = { 434 \cdot 10^{-2} } \ \mathrm{kN}
            >>> v8 = Variable('F',None,'kN')
            >>> print v8
            F
    """

    name = ""  #: symbolic name
    unit = ""  #: physical unit
    #: string to be formatted by the numeric value (with '%' operation)
    format = "%.4g  "
    # : string to be formatted by physical unit string (with '%' operation)
    unit_format = r"\mathrm{%s}"
    #: exponent for scientific representation. If 0, then no scientific representation is performed
    exponent = 0

    def __init__(
        self,
        name,
        value=None,
        unit="",
        format="%.4g",
        unit_format=r"\mathrm{%s}",
        exponent=0,
    ):
        self.name = name
        self._value = value
        self.unit = unit
        self.format = format
        self.unit_format = unit_format
        self.exponent = exponent
        self.set_format()

    def _get_value(self):
        return self._value

    def _set_value(self, v):
        if v is None:
            self._value = None
        else:
            try:
                self._value = float(v)
            except ValueError:
                self._value = str(v).strip()

    # : numeric value. If value==None, than the Variable is considered as symbolic
    value = property(_get_value, _set_value)

    def set_format(self):
        v = self._value
        if v is None:
            return
        try:
            if float(v) < 1000:
                self.format = "%.4g"
            else:
                self.format = "%.0f"
        except ValueError:
            self.format = self.format

    def str_symbolic(self):
        """Returns string of symbolic representation of receiver (its name)

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.str_symbolic()
                {a_{22}}
        """
        return "{%s}" % self.name

    def str_substituted(self):
        """Returns string of numeric representation of receiver (its formatted value)

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.str_substituted()
                3.45
        """
        return self.str_result_with_unit()

    def str_result(self, format="", exponent=0):
        """Returns string of the result of the receiver (its formatted result)

        :param str format: how to format result if other than predefined in receiver is required
        :param int exponent: exponent the returned string if other than predefined in receiver is required
        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.str_result()
                3.45
        """
        if self.is_symbolic():
            return self.str_symbolic()
        f = format if format else self.format
        e = exponent if exponent != 0 else self.exponent
        result = self.value
        if type(result) is str:
            return rf" {result}"
        if e == 0:
            if result < -1000:
                return rf"\left( {result: .0f} \right)"
            elif result < 0.0:
                return rf"\left( {result: .4g} \right)"
            elif result < 1000:
                return rf"{result: .4g}"
            return rf"{result: .0f}"  # r'%s'%f%r
        val = self.value * math.pow(10, -e)
        if self.value < 0.0:
            return r"\left( %s %s \right)" % (f % val, "\cdot 10^{%d}" % e)
        return "{ %s %s }" % (f % val, "\cdot 10^{%d}" % e)

    def str_result_with_unit(self):
        r"""Returns string of the result of the receiver (its formatted result) ending with its units

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.str_result_with_unit()
                3.45 \ \mathrm{mm}
        """
        return "%s \\ %s" % (self.str_result(), self.unit_format % self.unit)

    def result(self):
        """Returns numeric result of the receiver (its value)

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.result()
                3.45
        """
        if self.is_symbolic():
            raise LaTeXExpressionError("Unknown result of symbolic variable")
        return self.value

    def __float__(self):
        """Returns numeric result of the receiver

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print float(v1)
                3.45
        """
        return float(self.result())

    def __int__(self):
        """Returns numeric result of the receiver

        :rtype: int

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print int(v1)
                3
        """
        return int(float(self))

    def __str__(self):
        r"""Returns string representation of receiver in the form "name = value unit"

        :rtype: str

        .. code-block:: python

                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> print str(v3)
                F = { 434 \cdot 10^{-2} } \ \mathrm{kN}
                >>> v8 = Variable('F',None,'kN')
                >>> print str(v8)
                F
        """
        if self.is_symbolic():
            return "%s" % (self.name)
        return "%s = %s" % (self.name, self.str_result_with_unit())

    def to_latex_variable(self, name, what="float", command="def"):
        r"""Returns latex expression converting receiver to LaTeX variable using \def, \newcommand, or \renewcommand LaTeX command

        :param str name: LaTeX name (without initial \\ symbol)
        :param str what: what to include ('float' for numeric value, 'str' for string value (with possible scientific .10^x), 'valunit' for string value + unit , 'all' for str(self)'
        :param str command: LaTeX command to use (without initial \\ symbol) ['def','newcommand','renewcommand']

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> print v1.to_latex_variable('AA','float')
                \def\AA{3.45}
                >>> print v1.to_latex_variable('AA','str','newcommand')
                \newcommand{\AA}{3.45}
                >>> print v1.to_latex_variable('AA','valunit','renewcommand')
                \renewcommand{\AA}{3.45 \ \mathrm{mm}}
                >>> print v1.to_latex_variable('AA','all','def')
                \def\AA{a_{22} = 3.45 \ \mathrm{mm}}
        """
        what = what.lower()
        whats = ("float", "str", "valunit", "all", "subst")
        if not what in whats:
            raise LaTeXExpressionError("%s not in %s" % (what, whats))
        val = (
            self.value
            if what == "float"
            else (
                self.str_result()
                if what == "str"
                else (
                    self.str_result_with_unit()
                    if what == "valunit"
                    else str(self) if what == "all" or what == "subst" else None
                )
            )
        )
        return to_latex_variable(name, val, command)

    def to_latex_variable_float(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='float'"""
        return self.to_latex_variable(name, what="float", command=command)

    def to_latex_variable_str(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='str'"""
        return self.to_latex_variable(name, what="str", command=command)

    def to_latex_variable_val_unit(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='valunit'"""
        return self.to_latex_variable(name, what="valunit", command=command)

    def to_latex_variable_all(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='all'"""
        return self.to_latex_variable(name, what="all", command=command)

    def from_expression(self, expr):
        """Copy information from given Expression or Variable. Returns changed receiver

        :param Variable|Expression expr: given expression to be copied
        :rtype: Variable"""
        self.name = expr.name
        self.value = None if expr.is_symbolic() else float(expr)
        self.unit = expr.unit
        self.format = expr.format
        self.unit_format = expr.unit_format
        self.exponent = expr.exponent
        return self

    def is_symbolic(self):
        """Returns if receiver (or at least one of its sub-components) is purely symbolic variable without specific value"""
        return self.value is None

    def __add__(self, other):
        return _add(self, other)

    def __sub__(self, other):
        return _sub(self, other)

    def __mul__(self, other):
        return _mul(self, other)

    def __truediv__(self, other):
        return _div(self, other)

    def __floordiv__(self, other):
        return _div2(self, other)

    def __pow__(self, other):
        return _pow(self, other)

    def __radd__(self, other):
        return _radd(self, other)

    def __rsub__(self, other):
        return _rsub(self, other)

    def __rmul__(self, other):
        return _rmul(self, other)

    def __rtruediv__(self, other):
        return _rtruediv(self, other)

    def __rfloordiv__(self, other):
        return _rdiv2(self, other)

    def __rpow__(self, other):
        return _rpow(self, other)

    def __neg__(self):
        return _neg(self)

    def __pos__(self):
        return _pos(self)

    def __abs__(self):
        return _abs(self)


######################################################################


######################################################################
# Operation class
######################################################################
_NONE = ""
_ADD = "+"
_SUB = "-"
_MUL = "*"
_DIV = "/"
_DIV2 = "//"
_NEG = "neg"
_POS = "pos"
_ABS = "abs"
_MAX = "max"
_MIN = "min"
_POW = "pow"
_SQR = "sqr"
_ROOT = "root"
_SQRT = "sqrt"
_SIN = "sin"
_COS = "cos"
_TAN = "tan"
_SINH = "sinh"
_COSH = "cosh"
_TANH = "tanh"
_EXP = "exp"
_LOG = "log"
_LN = "ln"
_LOG10 = "log10"
_RBRACKETS = "()"
_SBRACKETS = "[]"
_CBRACKETS = "{}"
_ABRACKETS = "<>"

_supportedOperations1 = (
    _NONE,
    _NEG,
    _POS,
    _ABS,
    _SQR,
    _SQRT,
    _SIN,
    _COS,
    _TAN,
    _SINH,
    _COSH,
    _TANH,
    _EXP,
    _LN,
    _LOG10,
    _RBRACKETS,
    _SBRACKETS,
    _CBRACKETS,
    _ABRACKETS,
)
_supportedOperations2 = (_SUB, _DIV, _DIV2, _POW, _ROOT, _LOG)
_supportedOperationsN = (_ADD, _MUL, _MAX, _MIN)
_supportedOperations = (
    _supportedOperations1 + _supportedOperations2 + _supportedOperationsN
)


class Operation(object):
    r"""Class representing mathematical operation applied to one, two or more objects. These objects may be of type Variable, Expression or Operation again, allowing builing a hieararchy of operations. Preferable way of creation of Operation instances is to use predefined functions (see :ref:`predefinedOperations`) or (where it is possible) standard Python operations +,-,*,/,**.

    :param str type: type of operation
    :param Variable(s)|Expression(s)|Operation(s) args: Variables, Expressions, Operations to be combined

    .. code-block:: python

            >>> v1 = Variable('a_{22}',3.45,'mm')
            >>> v2 = Variable('F',5.876934835,'kN')
            >>> v3 = Variable('F',4.34,'kN',exponent=-2)
            >>> v4 = Variable('F',2.564345,'kN',format='%.4f')
            >>> v5 = Variable('F',5.876934835,'kN')
            >>> v6 = Variable('F',-6.543,'kN')
            >>> v8 = Variable('F',None,'kN')
            >>> o3 = (v1+v2)/v3
            >>> print o3
            \frac{ {a_{22}} + {F} }{ {F} } = \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } }
            >>> o4 = v1 + v8
            >>> print o4
            {a_{22}} + {F}
            >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
            >>> o2 = mul(r_brackets(e2+v4),v5,v6)
            >>> print o2
            \left( {E_2} + {F} \right) \cdot {F} \cdot {F} = \left( 2.14906 + 2.5643 \right) \cdot 5.87693 \cdot \left( -6.543 \right)
            >>> v8.value=2.34
            >>> print o4
            {a_{22}} + {F} = 3.45 + 2.34
    """

    type = None  #: arithmetic type of operation
    args = []  #: argument list subjected to the operation :py:attr:`Operation.type`
    format = "%.4g"  # see :py:attr:`Variable.format`
    exponent = 0  # see :py:attr:`Variable.exponent`

    def __init__(self, type, *args):
        if not type in _supportedOperations:
            raise LaTeXExpressionError(
                "operation %s not in supported operations %s"
                % (type, str(_supportedOperations))
            )
        self.type = type
        self.args = self.__check_args(args)
        self.format = "%.4g"
        self.exponent = 0

    def __check_args(self, args):
        ret = []
        for a in args:
            if isinstance(a, (Variable, Operation)):
                ret.append(a)
            elif isinstance(a, Expression):
                ret.append(a.to_variable())
            elif isinstance(a, int):
                ret.append(Variable("%d" % a, a, format="%d"))
            elif isinstance(a, float):
                ret.append(Variable("%.4g" % a, a, format="%.4g"))
            else:
                raise TypeError(
                    "wrong argument type (%s) in Operation constructor"
                    % a.__class__.__name__
                )
        return ret

    def __str(self, what):
        # auxiliary function to format symbolic or substituted expression. Both are the same, the only difference os to call str_symbolic or str_substituted on receiver args
        a = self.args
        t = self.type
        if t in _supportedOperationsN:
            v = (getattr(arg, what)() for arg in a)
            if t == _ADD:
                return r" + ".join(v)
            if t == _MUL:
                return r" \cdot ".join(v)
            if t == _MAX:
                return r"\max{\left( %s \right)}" % (", ".join(v))
            if t == _MIN:
                return r"\min{\left( %s \right)}" % (", ".join(v))
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        if t in _supportedOperations2:
            v0 = getattr(a[0], what)()
            v1 = getattr(a[1], what)()
            if t == _SUB:
                return r"%s - %s" % (v0, v1)
            if t == _DIV:
                return r"\frac{ %s }{ %s }" % (v0, v1)
            if t == _DIV2:
                return r"\left \lfloor \frac{ %s }{ %s } \right \rfloor" % (v0, v1)
            if t == _POW:
                return r"{\left( %s \right)}^{ %s }" % (v0, v1)
            if t == _ROOT:
                return r"\sqrt[ %s ]{ %s }" % (v0, v1)
            if t == _LOG:
                return r"\log_{ %s }{ %s }" % (v0, v1)
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        if t in _supportedOperations1:
            v = getattr(a[0], what)()
            if t == _NONE:
                return v
            if t == _NEG:
                return r"\left( - %s \right)" % v
            if t == _POS:
                return r"\left( + %s \right)" % v
            if t == _ABS:
                return r"\left| %s \right|" % v
            if t == _SQR:
                return r"%s^2" % v
            if t == _SQRT:
                return r"\sqrt{ %s }" % v
            if t == _SIN:
                return r"\sin{\left( %s \right)}" % v
            if t == _COS:
                return r"\cos{\left( %s \right)}" % v
            if t == _TAN:
                return r"\tan{\left( %s \right)}" % v
            if t == _SINH:
                return r"\sinh{\left( %s \right)}" % v
            if t == _COSH:
                return r"\cosh{\left( %s \right)}" % v
            if t == _TANH:
                return r"\tanh{\left( %s \right)}" % v
            if t == _EXP:
                return r"\mathrm{e}^{ %s }" % v
            if t == _LN:
                return r"\ln{ %s }" % v
            if t == _LOG10:
                return r"\log_{10}{ %s }" % v
            if t == _RBRACKETS:
                return r"\left( %s \right)" % v
            if t == _SBRACKETS:
                return r"\left[ %s \right]" % v
            if t == _CBRACKETS:
                return r"\left\{ %s \right\}" % v
            if t == _ABRACKETS:
                return r"\left\langle %s \right\rangle" % v
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        raise LaTeXExpressionError(
            "operation %s not in supported operations %s"
            % (self.type, str(_supportedOperations))
        )

    def str_symbolic(self):
        r"""Returns string of symbolic representation of receiver

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print o3.str_symbolic()
                \frac{ {a_{22}} + {F} }{ {F} }
        """
        return self.__str("str_symbolic")

    def str_substituted(self):
        r"""Returns string of substituted representation of receiver

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print o3.str_substituted()
                \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } }
        """
        return self.__str("str_substituted")

    def str_result(self, format="", exponent=0):
        """Returns string of the result of the receiver (its formatted result)

        :param str format: how to format result if other than predefined in receiver is required
        :param int exponent: exponent the returned string if other than predefined in receiver is required
        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print o3.str_result()
                2.14906
        """
        if self.is_symbolic():
            return self.str_symbolic()
        r = float(self)
        f = format if format else self.format
        e = exponent if exponent != 0 else self.exponent
        if e == 0:
            if r < -1000:
                return rf"\left( {r: .0f} \right)"
            elif r < 0:
                return r"\left(%s\right)" % f % r
            elif r < 1000:
                return rf"{r: .4g}"
            return rf"{r: .0f}"
        val = r * math.pow(10, -e)
        if r < 0.0:
            return r"\left( %s %s \right)" % (f % val, "\cdot 10^{%d}" % e)
        return "{ %s %s }" % (f % val, "\cdot 10^{%d}" % e)

    def result(self):
        """Returns numeric result of the receiver

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print o3.result()
                2.14906332604
        """
        a = self.args
        t = self.type
        if t in _supportedOperationsN:
            v = (float(arg) for arg in a)
            if t == _ADD:
                return sum(v)
            if t == _MUL:
                return reduce(lambda x, y: x * y, v, 1.0)
            if t == _MAX:
                return max(v)
            if t == _MIN:
                return min(v)
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        if t in _supportedOperations2:
            v0 = float(a[0])
            v1 = float(a[1])
            if t == _SUB:
                return v0 - v1
            if t == _DIV:
                return v0 / v1
            if t == _DIV2:
                return v0 // v1
            if t == _POW:
                return math.pow(v0, v1)
            if t == _ROOT:
                return math.pow(v1, 1.0 / v0)
            if t == _LOG:
                return math.log(v1) / math.log(v0)
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        if t in _supportedOperations1:
            v = float(a[0])
            if t == _NONE:
                return v
            if t == _NEG:
                return -v
            if t == _POS:
                return v
            if t == _ABS:
                return abs(v)
            if t == _SQR:
                return math.pow(v, 2)
            if t == _SQRT:
                return math.sqrt(v)
            if t == _SIN:
                return math.sin(v)
            if t == _COS:
                return math.cos(v)
            if t == _TAN:
                return math.tan(v)
            if t == _SINH:
                return math.sinh(v)
            if t == _COSH:
                return math.cosh(v)
            if t == _TANH:
                return math.tanh(v)
            if t == _EXP:
                return math.exp(v)
            if t == _LN:
                return math.log(v)
            if t == _LOG10:
                return math.log(v) / math.log(10)
            if t == _RBRACKETS:
                return v
            if t == _SBRACKETS:
                return v
            if t == _CBRACKETS:
                return v
            if t == _ABRACKETS:
                return v
            if _DEBUG:
                print(t)
                raise LaTeXExpressionError(t)
        raise LaTeXExpressionError(
            "operation %s not in supported operations %s"
            % (self.type, str(_supportedOperations))
        )

    def str_result_with_unit(self):
        r"""Returns string of the result of the receiver (its formatted result) ending with its units"""
        return self.str_result()

    def __float__(self):
        """Returns numeric result of the receiver

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print float(o3)
                2.14906332604
        """
        return float(self.result())

    def __int__(self):
        """Returns numeric result of the receiver

        :rtype: int

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print int(o3)
                2
        """
        return int(float(self))

    def __str__(self):
        r"""Returns string representation of receiver in the form "symbolicExpr = substitutedExpr"

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> o3 = (v1+v2)/v3
                >>> print str(o3)
                \frac{ {a_{22}} + {F} }{ {F} } = \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } }
        """
        if self.is_symbolic():
            return self.str_symbolic()
        return "%s = %s" % (self.str_symbolic(), self.str_substituted())

    def to_variable(self, newName="", **kw):
        """Returns new Variable instance with attributes copied from receiver

        :param str newName: new name of returned variable
        :params dict kw: keyword arguments passed to Variable constructor
        :rtype: Variable"""
        return Variable(newName, float(self), **kw)

    def is_symbolic(self):
        """Returns if receiver (or at least one of its sub-components) is purely symbolic variable without specific value"""
        return any(arg.is_symbolic() for arg in self.args)

    def __add__(self, other):
        return _add(self, other)

    def __sub__(self, other):
        return _sub(self, other)

    def __mul__(self, other):
        return _mul(self, other)

    def __truediv__(self, other):
        return _div(self, other)

    def __floordiv__(self, other):
        return _div2(self, other)

    def __pow__(self, other):
        return _pow(self, other)

    def __radd__(self, other):
        return _radd(self, other)

    def __rsub__(self, other):
        return _rsub(self, other)

    def __rmul__(self, other):
        return _rmul(self, other)

    def __rtruediv__(self, other):
        return _rtruediv(self, other)

    def __rfloordiv__(self, other):
        return _rdiv2(self, other)

    def __rpow__(self, other):
        return _rpow(self, other)

    def __neg__(self):
        return _neg(self)

    def __pos__(self):
        return _pos(self)

    def __iadd__(self, other):
        return _add(self, other)

    def __isub__(self, other):
        return _sub(self, other)

    def __imul__(self, other):
        return _mul(self, other)

    def __idiv__(self, other):
        return _div(self, other)

    def __ifloordiv__(self, other):
        return _div2(self, other)

    def __ineg__(self):
        return _neg(self)

    def __ipos__(self):
        return _pos(self)

    def __abs__(self):
        return _abs(self)


######################################################################


######################################################################
# Predefined function for Operation instances creation
######################################################################
def sum_elements(*args):
    """Returns addition Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 or more objects for summation ( arg0 + arg1 + ... + argLast)
    """
    return Operation(_ADD, *args)


add = sum_elements
plus = sum_elements
"""Alias for :func:`.sum_elements`"""


def sub(*args):
    """Returns subtraction Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for subtraction ( arg0 - arg1)
    """
    return Operation(_SUB, *args)


minus = sub
"""Alias for :func:`.sub`"""


def mul(*args):
    """Returns multiplication Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 or more objects for multiplication ( arg0 * arg1 * ... * argLast )
    """
    return Operation(_MUL, *args)


times = mul
"""Alias for :func:`.mul`"""


def div(*args):
    """Returns division Operation instance (in LaTeX marked by \\\\frac{...}{...})

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for division ( arg0 / arg1)
    """
    return Operation(_DIV, *args)


def div2(*args):
    """Returns floor division Operation instance (in LaTeX marked by \\\\frac{...}{...} within a floor operation)

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for floor division ( arg0 // arg1)
    """
    return Operation(_DIV2, *args)


def neg(*args):
    """Returns negation Operation instance

    :param Variable|Expression|Operation args: 1 objects for negation ( -arg0)"""
    return Operation(_NEG, *args)


def pos(*args):
    """Returns the "positivition" (which does nothing actually) Operation instance

    :param Variable|Expression|Operation args: 1 object"""
    return Operation(_POS, *args)


def absolute(*args):
    """Returns absolute value Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 1 objects for absolute value ( \|arg0\| )
    """
    return Operation(_ABS, *args)


def maximum(*args):
    """Returns max Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for max ( max(arg0,arg1,...,argN) )
    """
    return Operation(_MAX, *args)


def minimum(*args):
    """Returns min Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for min ( min(arg0,arg1,...,argN) )
    """
    return Operation(_MIN, *args)


def power(*args):
    """Returns power Operation instance

    :param Variable(s)|Expression(s)|Operation(s) args: 2 objects for power ( arg0 ^ arg1)
    """
    return Operation(_POW, *args)


def sqr(*args):
    """Returns square Operation instance

    :param Variable|Expression|Operation args: 1 objects for square ( arg ^ 2)"""
    return Operation(_SQR, *args)


def root(*args):
    """Returns root Operation instance

    :param Variable|Expression|Operation args: 1 objects for square root ( arg1^(1/arg0) )
    """
    return Operation(_ROOT, *args)


def sqrt(*args):
    """Returns square root Operation instance

    :param Variable|Expression|Operation args: 1 objects for square root ( sqrt(arg) )
    """
    return Operation(_SQRT, *args)


def sin(*args):
    """Returns sinus Operation instance

    :param Variable|Expression|Operation args: 1 objects for sinus ( sin(arg) )"""
    return Operation(_SIN, *args)


def cos(*args):
    """Returns cosinus Operation instance

    :param Variable|Expression|Operation args: 1 objects for cosinus ( cos(arg) )"""
    return Operation(_COS, *args)


def tan(*args):
    """Returns tangent Operation instance

    :param Variable|Expression|Operation args: 1 objects for tangent ( tan(arg) )"""
    return Operation(_TAN, *args)


def sinh(*args):
    """Returns hyperbolic sinus Operation instance

    :param Variable|Expression|Operation args: 1 objects for hyperbolic sinus ( sin(arg) )
    """
    return Operation(_SINH, *args)


def cosh(*args):
    """Returns hyperbolic cosinus Operation instance

    :param Variable|Expression|Operation args: 1 objects for hyperbolic cosinus ( cos(arg) )
    """
    return Operation(_COSH, *args)


def tanh(*args):
    """Returns hyperbolic tangent Operation instance

    :param Variable|Expression|Operation args: 1 objects for hyperbolic tangent ( tan(arg) )
    """
    return Operation(_TANH, *args)


def exp(*args):
    """Returns exp Operation instance

    :param Variable|Expression|Operation args: 1 objects for exp ( exp(arg)=e^arg )"""
    return Operation(_EXP, *args)


def log(*args):
    """Returns logarithm Operation instance

    :param Variable|Expression|Operation args: 2 objects for logarithm ( log_arg0(arg1) = ln(arg1)/ln(arg0) )
    """
    return Operation(_LOG, *args)


def ln(*args):
    """Returns natural logarithm Operation instance

    :param Variable|Expression|Operation args: 1 objects for natural logarithm ( ln(arg) )
    """
    return Operation(_LN, *args)


def log10(*args):
    """Returns decadic logarithm Operation instance

    :param Variable|Expression|Operation args: 1 objects for decadic logarithm ( log_10(arg) )
    """
    return Operation(_LOG10, *args)


def r_brackets(*args):
    """Returns round brackets Operation instance (wraps passed argument to round brackets)

    :param Variable|Expression|Operation args: 1 objects for round brackets ( (arg) )"""
    return Operation(_RBRACKETS, *args)


brackets = r_brackets
"""Alias for :func:`.r_brackets`"""


def s_brackets(*args):
    """Returns square brackets Operation instance (wraps passed argument to square brackets)

    :param Variable|Expression|Operation args: 1 objects for square brackets ( [arg] )
    """
    return Operation(_SBRACKETS, *args)


def c_brackets(*args):
    """Returns curly brackets Operation instance (wraps passed argument to curly brackets)

    :param Variable|Expression|Operation args: 1 objects for curly brackets ( {arg} )"""
    return Operation(_CBRACKETS, *args)


def a_brackets(*args):
    """Returns angle brackets Operation instance (wraps passed argument to angle brackets)

    :param Variable|Expression|Operation args: 1 objects for angle brackets ( ⟨arg⟩ )"""
    return Operation(_ABRACKETS, *args)


######################################################################


######################################################################
# Expression class
######################################################################
class Expression(object):
    r"""Class representing mathematical expression

    :param str name: symbolic name of the expression
    :param Operation|Variable|Expression operation: operation of the expression
    :param str unit: physical unit of the expression
    :param str format: python string to be formatted with '%' operation (e.g. '%e', '%g', '%.4g', '%.3f' etc.). See `Python string formatting docs <http://docs.python.org/2/library/stdtypes.html#string-formatting-operations>`_ for more details.
    :param str unit_format: python string to be formatted with unit (default is '\mathrm{%s}' for non-italic units inside math mode). For no formatting use '%s'. See `Python string formatting docs <http://docs.python.org/2/library/stdtypes.html#string-formatting-operations>`_ for more details.
    :param int exponent: exponent for scientific representation

    .. code-block:: python

            >>> v1 = Variable('a_{22}',3.45,'mm')
            >>> v2 = Variable('F',5.876934835,'kN')
            >>> v3 = Variable('F',4.34,'kN',exponent=-2)
            >>> v4 = Variable('F',2.564345,'kN',format='%.4f')
            >>> v5 = Variable('F',5.876934835,'kN')
            >>> v6 = Variable('F',-6.543,'kN')
            >>> v8 = Variable('F',None,'kN')
            >>> o1 = (v1 + sqrt(v2)) / (v3 * v4) + v5
            >>> e1 = Expression('E_1^i',s_brackets(o1) - sqr(v6),'kNm')
            >>> print e1
            E_1^i = \left[ \frac{ {a_{22}} + \sqrt{ {F} } }{ {F} \cdot {F} } + {F} \right] - {F}^2 = \left[ \frac{ 3.45 + \sqrt{ 5.87693 } }{ { 434 \cdot 10^{-2} } \cdot 2.5643 } + 5.87693 \right] - \left( -6.543 \right)^2 = \left(-36.4061\right) \ \mathrm{kNm}
            >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
            >>> print e2
            E_2 = \frac{ {a_{22}} + {F} }{ {F} } = \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } } = 2.14906 \ \mathrm{mm}
            >>> o4 = v1 + v8
            >>> e4 = Expression('E_4',o4,'mF')
            >>> print e4
            E_4 = {a_{22}} + {F}
            >>> v8.value=2.34
            >>> print e4
            E_4 = {a_{22}} + {F} = 3.45 + 2.34 = 5.79 \ \mathrm{mF}
    """

    name = ""  #: symbolic name of the expression
    operation = None  #: underlying :class:`.Operation` instance
    unit = ""  #: see :py:attr:`Variable.unit`
    format = "%.4g"  #: see :py:attr:`Variable.format`
    unit_format = r"\mathrm{%s}"  # : see :py:attr:`Variable.unit_format`
    exponent = 0  #: see :py:attr:`Variable.exponent`

    def __init__(
        self,
        name,
        operation,
        unit="",
        format="%.4g",
        unit_format=r"\mathrm{%s}",
        exponent=0,
    ):
        self.name = name
        self.operation = (
            Operation(_NONE, operation)
            if isinstance(operation, Variable)
            else operation
        )
        self.unit = unit
        self.format = format
        self.unit_format = unit_format
        self.exponent = exponent
        self.set_format()

    def _get_operation(self):
        return self.operation

    def _set_operation(self, o):
        self.operation = o

    # : Shortcut for :py:meth:`operation <Expression.operation>`
    o = property(_get_operation, _set_operation)

    def set_format(self):
        v = self.str_result()
        try:
            if float(v) < 1000:
                self.format = "%.4g"
            else:
                self.format = "%.0f"
        except ValueError:
            self.format = self.format

    def str_symbolic(self):
        """Returns string of symbolic representation of receiver (its name)

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.str_symbolic()
                {E_2}
        """
        return "{%s}" % self.name

    def str_substituted(self):
        """Returns string of numeric representation of receiver (its formatted result)

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.str_substituted()
                2.14906
        """
        return self.str_result()

    def str_result(self, format="", exponent=0):
        """Returns string of the result of the receiver (its formatted result)

        :param str format: how to format result if other than predefined in receiver is required
        :param int exponent: exponent the returned string if other than predefined in receiver is required
        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.str_result()
                2.14906
        """
        if self.is_symbolic():
            return self.operation.str_substituted()
        r = float(self)
        f = format if format else self.format
        e = exponent if exponent != 0 else self.exponent
        if e == 0:
            if r < -1000:
                return rf"\left( {r: .0f} \right)"
            elif r < 0:
                return r"\left(%s\right)" % f % r
            elif r < 1000:
                return rf"{r: .4g}"
            return rf"{r: .0f}"
        val = float(self) * math.pow(10, -e)
        if r < 0:
            return r"\left( %s %s \right)" % (f % val, "\cdot 10^{%d}" % e)
        return "{ %s %s }" % (f % val, "\cdot 10^{%d}" % e)

    def str_result_with_unit(self):
        r"""Returns string of the result of the receiver (its formatted result) ending with its units

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.str_result_with_unit()
                2.14906 \ \mathrm{mm}
        """
        return "%s \\ %s" % (self.str_result(), self.unit_format % self.unit)

    def result(self):
        """Returns numeric result of the receiver

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.result()
                2.14906332604
        """
        return float(self.operation)

    def __float__(self):
        """Returns numeric result of the receiver

        :rtype: float

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print float(e2)
                2.14906332604
        """
        return float(self.result())

    def __int__(self):
        """Returns numeric result of the receiver

        :rtype: int

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print int(e2)
                2
        """
        return int(float(self))

    def to_variable(self, newName=""):
        """Returns new Variable instance with attributes copied from receiver

        :param str newName: optional new name of returned variable
        :rtype: Variable"""
        ret = Variable("", 0, "").from_expression(self)
        if newName:
            ret.name = newName
        return ret

    def __str__(self):
        r"""Returns string representation of receiver in the form "name = symbolicExpr = substitutedExpr = result unit"

        :rtype: str

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print str(e2)
                E_2 = \frac{ {a_{22}} + {F} }{ {F} } = \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } } = 2.14906 \ \mathrm{mm}
        """
        if self.is_symbolic():
            return "%s = %s" % (self.name, self.operation)
        return "%s = %s = %s" % (self.name, self.operation, self.str_result_with_unit())

    def to_latex_variable(self, name, what="float", command="def"):
        r"""Returns latex expression converting receiver to LaTeX variable using \def, \newcommand, or \renewcommand LaTeX command

        :param str name: LaTeX name (without initial \\ symbol)
        :param str what: what to include ('float' for numeric value, 'str' for string value (with possible scientific .10^x), 'valunit' for string value + unit , 'symb' for symbolic expression, 'subst' for substrituted expression and 'all' for str(self)'
        :param str command: LaTeX command to use (without initial \\ symbol) ['def','newcommand','renewcommand']

        .. code-block:: python

                >>> v1 = Variable('a_{22}',3.45,'mm')
                >>> v2 = Variable('F',5.876934835,'kN')
                >>> v3 = Variable('F',4.34,'kN',exponent=-2)
                >>> e2 = Expression('E_2',(v1+v2)/v3,'mm')
                >>> print e2.to_latex_variable('ETWO','float')
                \def\ETWO{2.14906332604}
                >>> print e2.to_latex_variable('ETWO','str','newcommand')
                \newcommand{\ETWO}{2.14906}
                >>> print e2.to_latex_variable('ETWO','valunit','renewcommand')
                \renewcommand{\ETWO}{2.14906 \ \mathrm{mm}}
                >>> print e2.to_latex_variable('ETWO','symb')
                \def\ETWO{{E_2}}
                >>> print e2.to_latex_variable('ETWO','subst')
                \def\ETWO{2.14906}
                >>> print e2.to_latex_variable('ETWO','all','def')
                \def\ETWO{E_2 = \frac{ {a_{22}} + {F} }{ {F} } = \frac{ 3.45 + 5.87693 }{ { 434 \cdot 10^{-2} } } = 2.14906 \ \mathrm{mm}}
        """
        what = what.lower()
        whats = ("float", "str", "valunit", "symb", "subst", "all")
        if not what in whats:
            raise LaTeXExpressionError("%s not in %s" % (what, whats))
        val = (
            float(self)
            if what == "float"
            else (
                self.str_result()
                if what == "str"
                else (
                    self.str_result_with_unit()
                    if what == "valunit"
                    else (
                        self.str_symbolic()
                        if what == "symb"
                        else (
                            self.str_substituted()
                            if what == "subst"
                            else str(self) if what == "all" else None
                        )
                    )
                )
            )
        )
        return to_latex_variable(name, val, command)

    def to_latex_variable_float(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='float'"""
        return self.to_latex_variable(name, what="float", command=command)

    def to_latex_variable_str(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='str'"""
        return self.to_latex_variable(name, what="str", command=command)

    def to_latex_variable_val_unit(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='valunit'"""
        return self.to_latex_variable(name, what="valunit", command=command)

    def to_latex_variable_symb(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='symb'"""
        return self.to_latex_variable(name, what="symb", command=command)

    def to_latex_variable_subst(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='subst'"""
        return self.to_latex_variable(name, what="subst", command=command)

    def to_latex_variable_all(self, name, command="def"):
        """Shortcut for :meth:`.Variable.to_latex_variable` with what='all'"""
        return self.to_latex_variable(name, what="all", command=command)

    def is_symbolic(self):
        """Returns if receiver (or at least one of its sub-components) is purely symbolic variable without specific value"""
        return self.operation.is_symbolic()

    def __add__(self, other):
        return _add(self, other)

    def __sub__(self, other):
        return _sub(self, other)

    def __mul__(self, other):
        return _mul(self, other)

    def __truediv__(self, other):
        return _div(self, other)

    def __floordiv__(self, other):
        return _div2(self, other)

    def __pow__(self, other):
        return _pow(self, other)

    def __radd__(self, other):
        return _radd(self, other)

    def __rsub__(self, other):
        return _rsub(self, other)

    def __rmul__(self, other):
        return _rmul(self, other)

    def __rtruediv__(self, other):
        return _rtruediv(self, other)

    def __rfloordiv__(self, other):
        return _rdiv2(self, other)

    def __rpow__(self, other):
        return _rpow(self, other)

    def __neg__(self):
        return _neg(self)

    def __pos__(self):
        return _pos(self)

    def __abs__(self):
        return _abs(self)


######################################################################


######################################################################
# Predefined variable instances
######################################################################
ZERO = Variable("0", 0.0, format="%d")
"""Variable instance representing 1"""
ONE = Variable("1", 1.0, format="%d")
"""Variable instance representing 1"""
TWO = Variable("2", 2.0, format="%d")
"""Variable instance representing 2"""
E = Variable("\mathrm{e}", math.e)
"""Variable instance representing Euler number"""
PI = Variable("\pi", math.pi)
"""Variable instance representing pi"""


######################################################################


######################################################################
# other functions
######################################################################
def save_vars(what, fileName="/tmp/latexexprglobals.out"):
    """Saves globally defined variables from current session into a file. This simplifies working within one LaTeX document, but several python sessions

    :param dict what: dictionary object (like locals() or globals()) to be saved
    :param string fileName: name of file to save the variables
    """
    # http://stackoverflow.com/questions/2960864/how-can-i-save-all-the-variables-in-the-current-python-session
    import shelve

    my_shelf = shelve.open(fileName, "n")  # 'n' for new
    for key in what:
        if key.startswith("__") and key.endswith("__"):
            continue
        try:
            my_shelf[key] = what[key]
        except (TypeError, KeyError):
            # __builtins__, my_shelf, and imported modules can not be shelved.
            pass
    my_shelf.close()


def load_vars(what, fileName="/tmp/latexexprglobals.out"):
    """Loads saved variables form a file into global namespace

    :param dict what: dictionary object (like locals() or globals()) that will be updated with laded values
    :param string fileName: name of file with saved variables
    """
    # http://stackoverflow.com/questions/2960864/how-can-i-save-all-the-variables-in-the-current-python-session
    import shelve

    my_shelf = shelve.open(fileName)
    for key in my_shelf:
        what[key] = my_shelf[key]
    my_shelf.close()


def to_latex_variable(name, what, command="def"):
    r"""Returns latex expression converting receiver to LaTeX variable using \def, \newcommand, or \renewcommand LaTeX command

    :param str name: LaTeX name (without initial \\ symbol)
    :param str what: string of the variable body
    :param str command: LaTeX command to use (without initial \\ symbol) ['def','newcommand','renewcommand']

    .. code-block:: python

                    >>> n,s = 'varName','some string content of the variable'
                    >>> print to_latex_variable(n,s)
                    \def\varName{some string content of the variable}
                    >>> print to_latex_variable(n,s,'newcommand')
                    \newcommand{\varName}{some string content of the variable}
                    >>> print to_latex_variable(n,s,'renewcommand')
                    \renewcommand{\varName}{some string content of the variable}
    """
    if command == "def":
        return r"\def\%s{%s}" % (name, what)
    elif command == "newcommand" or command == "renewcommand":
        return r"\%s{\%s}{%s}" % (command, name, what)
    else:
        raise LaTeXExpressionError(
            "to_latex_variable: wrong command parameter (should be in ['def','newcommand','renewcommand']"
        )


######################################################################


# TESTING
if __name__ == "__main__":
    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1)
    v2 = Variable("F", 5.876934835, "kN")
    print(v2)
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    print(v3)
    v4 = Variable("F", 2.564345, "kN", format="%.4f")
    print(v4)
    v5 = Variable("F", 5.876934835, "kN")
    print(v5)
    v6 = Variable("F", -6.543, "kN")
    o1 = (v1 + sqrt(v2)) / (v3 * v4) + v5
    print(o1)
    e1 = Expression("E_1^i", s_brackets(o1) - sqr(v6), "kNm")
    print(e1)
    v7 = e1.to_variable()
    print(v7)
    print(v7.to_latex_variable_all("MYV7"))
    v8 = Variable("F", None, "kN")
    o4 = v1 + v8
    e4 = Expression("E_4", o4, "mF")
    print(v8)
    print(o4)
    print(e4)
    v8.value = 2.34
    print(v8)
    print(o4)
    print(e4)

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1)
    v2 = Variable("F", 5.876934835, "kN")
    print(v2)
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    print(v3)
    v8 = Variable("F", None, "kN")
    print(v8)

    v3 = Variable("F", 4.34, "kN", exponent=-2)
    print(str(v3))
    v8 = Variable("F", None, "kN")
    print(str(v8))

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.str_symbolic())

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.str_substituted())

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.str_result())

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.str_result_with_unit())

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.result())

    v1 = Variable("a_{22}", 3.45, "mm")
    print(float(v1))

    v1 = Variable("a_{22}", 3.45, "mm")
    print(int(v1))

    v1 = Variable("a_{22}", 3.45, "mm")
    print(v1.to_latex_variable("AA", "float"))
    print(v1.to_latex_variable("AA", "str", "newcommand"))
    print(v1.to_latex_variable("AA", "valunit", "renewcommand"))
    print(v1.to_latex_variable("AA", "all", "def"))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    v4 = Variable("F", 2.564345, "kN", format="%.4f")
    v5 = Variable("F", 5.876934835, "kN")
    v6 = Variable("F", -6.543, "kN")
    v8 = Variable("F", None, "kN")
    o3 = (v1 + v2) / v3
    print(o3)
    o4 = v1 + v8
    print(o4)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    o2 = mul(r_brackets(e2 + v4), v5, v6)
    print(o2)
    v8.value = 2.34
    print(o4)

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(str(o3))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(o3.str_symbolic())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(o3.str_substituted())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(o3.str_result())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(o3.result())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(float(o3))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    o3 = (v1 + v2) / v3
    print(int(o3))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    v4 = Variable("F", 2.564345, "kN", format="%.4f")
    v5 = Variable("F", 5.876934835, "kN")
    v6 = Variable("F", -6.543, "kN")
    v8 = Variable("F", None, "kN")
    o1 = (v1 + sqrt(v2)) / (v3 * v4) + v5
    e1 = Expression("E_1^i", s_brackets(o1) - sqr(v6), "kNm")
    print(e1)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2)
    o4 = v1 + v8
    e4 = Expression("E_4", o4, "mF")
    print(e4)
    v8.value = 2.34
    print(e4)

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(str(e2))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.str_symbolic())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.str_substituted())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.str_result())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.str_result_with_unit())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.result())

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(float(e2))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(int(e2))

    v1 = Variable("a_{22}", 3.45, "mm")
    v2 = Variable("F", 5.876934835, "kN")
    v3 = Variable("F", 4.34, "kN", exponent=-2)
    e2 = Expression("E_2", (v1 + v2) / v3, "mm")
    print(e2.to_latex_variable("ETWO", "float"))
    print(e2.to_latex_variable("ETWO", "str", "newcommand"))
    print(e2.to_latex_variable("ETWO", "valunit", "renewcommand"))
    print(e2.to_latex_variable("ETWO", "symb"))
    print(e2.to_latex_variable("ETWO", "subst"))
    print(e2.to_latex_variable("ETWO", "all", "def"))

    n, s = "varName", "some string content of the variable"
    print(to_latex_variable(n, s))
    print(to_latex_variable(n, s, "newcommand"))
    print(to_latex_variable(n, s, "renewcommand"))
######################################################################
