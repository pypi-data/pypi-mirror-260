import math

import pytest

from latexexpr_efficalc import (
    Operation,
    Variable,
    a_brackets,
    brackets,
    c_brackets,
    cos,
    cosh,
    exp,
    ln,
    log,
    log10,
    maximum,
    minimum,
    r_brackets,
    s_brackets,
    sin,
    sinh,
    sqrt,
    sum_elements,
    tan,
    tanh,
)


def test_variable_add():
    a = Variable("a", 5)
    c = a + a
    assert c.result() == 10


def test_variable_add_right():
    a = Variable("a", 5)
    c = 2 + a
    assert c.result() == 7


def test_variable_add_left():
    a = Variable("a", 5)
    c = a + 2
    assert c.result() == 7


def test_variable_subtract():
    a = Variable("a", 5)
    c = a - a
    assert c.result() == 0


def test_variable_subtract_right():
    a = Variable("a", 5)
    c = 7 - a
    assert c.result() == 2


def test_variable_subtract_left():
    a = Variable("a", 5)
    c = a - 7
    assert c.result() == -2


def test_variable_multiply():
    a = Variable("a", 5)
    c = a * a
    assert c.result() == 25


def test_variable_multiply_right():
    a = Variable("a", 5)
    c = 2 * a
    assert c.result() == 10


def test_variable_multiply_left():
    a = Variable("a", 5)
    c = a * 2
    assert c.result() == 10


def test_variable_power():
    a = Variable("a", 5)
    b = Variable("b", 3)
    c = a**b
    assert c.result() == 125


def test_variable_power_right():
    a = Variable("a", 5)
    c = 2**a
    assert c.result() == 32


def test_variable_power_left():
    a = Variable("a", 5)
    c = a**2
    assert c.result() == 25


def test_variable_divide():
    a = Variable("a", 5)
    c = a / a
    assert c.result() == 1


def test_variable_divide_right():
    a = Variable("a", 5)
    c = 10 / a
    assert c.result() == 2


def test_variable_divide_left():
    a = Variable("a", 5)
    c = a / 2
    assert c.result() == 2.5


def test_variable_floor_div():
    a = Variable("a", 5)
    b = Variable("b", 2)
    c = a // b
    assert c.result() == 2


def test_variable_neg():
    a = Variable("a", 5)
    assert (-a).result() == -5


def test_variable_abs():
    a = Variable("a", -5)
    assert abs(a).result() == 5


def test_variable_sum():
    a = Variable("a", 5)
    b = Variable("b", 15)
    c = Variable("c", 2)
    assert sum_elements(a, b, c).result() == 22


def test_variable_max():
    a = Variable("a", 5)
    b = Variable("b", 15)
    c = Variable("c", 2)
    assert maximum(a, b, c).result() == 15


def test_variable_min():
    a = Variable("a", 5)
    b = Variable("b", 15)
    c = Variable("c", 2)
    assert minimum(a, b, c).result() == 2


def test_variable_sqrt():
    a = Variable("a", 25)
    assert sqrt(a).result() == 5


def test_variable_sin():
    a = Variable("a", math.pi / 2)
    assert sin(a).result() == pytest.approx(1, abs=0.001)


def test_variable_cos():
    a = Variable("a", math.pi / 2)
    assert cos(a).result() == pytest.approx(0, abs=0.001)


def test_variable_tan():
    a = Variable("a", math.pi / 3)
    assert tan(a).result() == pytest.approx(1.732050, abs=0.001)


def test_variable_sinh():
    a = Variable("a", -2)
    assert sinh(a).result() == pytest.approx(-3.62686, abs=0.001)


def test_variable_cosh():
    a = Variable("a", -2)
    assert cosh(a).result() == pytest.approx(3.762196, abs=0.001)


def test_variable_tanh():
    a = Variable("a", -2)
    assert tanh(a).result() == pytest.approx(-0.96403, abs=0.001)


def test_variable_exp():
    a = Variable("a", 2)
    assert exp(a).result() == pytest.approx(math.e**2, abs=0.001)


def test_variable_log():
    a = Variable("a", 2)
    b = Variable("b", 64)
    assert log(a, b).result() == 6


def test_variable_ln():
    a = Variable("a", 2)
    assert ln(a).result() == pytest.approx(0.693147, abs=0.001)


def test_variable_log10():
    a = Variable("a", 10000)
    assert log10(a).result() == 4


def test_variable_r_brackets():
    a = Variable("a", 2)
    b = Variable("b", 3, "in")
    c = b * r_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right)"
    )


def test_variable_brackets():
    a = Variable("a", 2)
    b = Variable("b", 3, "in")
    c = b * brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left(  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right)"
    )


def test_variable_s_brackets():
    a = Variable("a", 2)
    b = Variable("b", 3, "in")
    c = b * s_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left[  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right]"
    )


def test_variable_c_brackets():
    a = Variable("a", 2)
    b = Variable("b", 3, "in")
    c = b * c_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left\\{  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right\\}"
    )


def test_variable_a_brackets():
    a = Variable("a", 2)
    b = Variable("b", 3, "in")
    c = b * a_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot \\left\\langle  2 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\right\\rangle"
    )
