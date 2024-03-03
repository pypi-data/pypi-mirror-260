import math

import pytest

from latexexpr_efficalc import (
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

VARIABLE_TO_OPERATION = Variable("one", 1)


def test_operation_add():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a + a
    assert c.result() == 10


def test_operation_add_right():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = 2 + a
    assert c.result() == 7


def test_operation_add_left():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a + 2
    assert c.result() == 7


def test_operation_subtract():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a - a
    assert c.result() == 0


def test_operation_subtract_right():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = 7 - a
    assert c.result() == 2


def test_operation_subtract_left():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a - 7
    assert c.result() == -2


def test_operation_multiply():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a * a
    assert c.result() == 25


def test_operation_multiply_right():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = 2 * a
    assert c.result() == 10


def test_operation_multiply_left():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a * 2
    assert c.result() == 10


def test_operation_power():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    b = Variable("b", 3) * VARIABLE_TO_OPERATION
    c = a**b
    assert c.result() == 125


def test_operation_power_right():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = 2**a
    assert c.result() == 32


def test_operation_power_left():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a**2
    assert c.result() == 25


def test_operation_divide():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a / a
    assert c.result() == 1


def test_operation_divide_right():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = 10 / a
    assert c.result() == 2


def test_operation_divide_left():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    c = a / 2
    assert c.result() == 2.5


def test_operation_floor_div():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    b = Variable("b", 2) * VARIABLE_TO_OPERATION
    c = a // b
    assert c.result() == 2


def test_operation_neg():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    assert (-a).result() == -5


def test_operation_abs():
    a = Variable("a", -5) * VARIABLE_TO_OPERATION
    assert abs(a).result() == 5


def test_operation_sum():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    b = Variable("b", 15) * VARIABLE_TO_OPERATION
    c = Variable("c", 2) * VARIABLE_TO_OPERATION
    assert sum_elements(a, b, c).result() == 22


def test_operation_max():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    b = Variable("b", 15) * VARIABLE_TO_OPERATION
    c = Variable("c", 2) * VARIABLE_TO_OPERATION
    assert maximum(a, b, c).result() == 15


def test_operation_min():
    a = Variable("a", 5) * VARIABLE_TO_OPERATION
    b = Variable("b", 15) * VARIABLE_TO_OPERATION
    c = Variable("c", 2) * VARIABLE_TO_OPERATION
    assert minimum(a, b, c).result() == 2


def test_operation_sqrt():
    a = Variable("a", 25) * VARIABLE_TO_OPERATION
    assert sqrt(a).result() == 5


def test_operation_sin():
    a = Variable("a", math.pi / 2) * VARIABLE_TO_OPERATION
    assert sin(a).result() == pytest.approx(1, abs=0.001)


def test_operation_cos():
    a = Variable("a", math.pi / 2) * VARIABLE_TO_OPERATION
    assert cos(a).result() == pytest.approx(0, abs=0.001)


def test_operation_tan():
    a = Variable("a", math.pi / 3) * VARIABLE_TO_OPERATION
    assert tan(a).result() == pytest.approx(1.732050, abs=0.001)


def test_operation_sinh():
    a = Variable("a", -2) * VARIABLE_TO_OPERATION
    assert sinh(a).result() == pytest.approx(-3.62686, abs=0.001)


def test_operation_cosh():
    a = Variable("a", -2) * VARIABLE_TO_OPERATION
    assert cosh(a).result() == pytest.approx(3.762196, abs=0.001)


def test_operation_tanh():
    a = Variable("a", -2) * VARIABLE_TO_OPERATION
    assert tanh(a).result() == pytest.approx(-0.96403, abs=0.001)


def test_operation_exp():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    assert exp(a).result() == pytest.approx(math.e**2, abs=0.001)


def test_operation_log():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 64) * VARIABLE_TO_OPERATION
    assert log(a, b).result() == 6


def test_operation_ln():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    assert ln(a).result() == pytest.approx(0.693147, abs=0.001)


def test_operation_log10():
    a = Variable("a", 10000) * VARIABLE_TO_OPERATION
    assert log10(a).result() == 4


def test_operation_r_brackets():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 3, "in") * VARIABLE_TO_OPERATION
    c = b * r_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\cdot \\left(  2 \\ \\mathrm{} \\cdot  1 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\right)"
    )


def test_operation_brackets():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 3, "in") * VARIABLE_TO_OPERATION
    c = b * brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\cdot \\left(  2 \\ \\mathrm{} \\cdot  1 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\right)"
    )


def test_operation_s_brackets():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 3, "in") * VARIABLE_TO_OPERATION
    c = b * s_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\cdot \\left[  2 \\ \\mathrm{} \\cdot  1 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\right]"
    )


def test_operation_c_brackets():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 3, "in") * VARIABLE_TO_OPERATION
    c = b * c_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\cdot \\left\\{  2 \\ \\mathrm{} \\cdot  1 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\right\\}"
    )


def test_operation_a_brackets():
    a = Variable("a", 2) * VARIABLE_TO_OPERATION
    b = Variable("b", 3, "in") * VARIABLE_TO_OPERATION
    c = b * a_brackets(a + b)
    assert c.result() == 15
    assert (
        c.str_substituted()
        == " 3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\cdot \\left\\langle  2 \\ \\mathrm{} \\cdot  1 \\ \\mathrm{} +  3 \\ \\mathrm{in} \\cdot  1 \\ \\mathrm{} \\right\\rangle"
    )
