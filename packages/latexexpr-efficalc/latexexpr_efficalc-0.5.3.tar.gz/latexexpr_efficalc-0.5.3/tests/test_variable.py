from latexexpr_efficalc import Variable


def test_none_value():
    assert Variable("a", None).value is None
    assert Variable("a", None).is_symbolic() is True
    assert Variable("a", None).str_result() == "{a}"
    assert Variable("a", None).str_symbolic() == "{a}"


def test_str_value():
    assert Variable("a", "test").value is "test"
    assert Variable("a", "test").is_symbolic() is False
    assert Variable("a", "test").str_result() == " test"
    assert Variable("a", "test").str_symbolic() == "{a}"


def test_int_value():
    assert Variable("a", 15).value == 15
    assert Variable("a", 15).is_symbolic() is False
    assert Variable("a", 15).str_result() == " 15"
    assert Variable("a", 15).str_symbolic() == "{a}"


def test_result():
    assert Variable("a", 0).result() == 0.0
    assert Variable("a", 3.9, "in").result() == 3.9
    assert Variable("a", 10**9, "in").result() == 10**9


def test_str_result():
    assert Variable("a", 0).str_result() == " 0"
    assert Variable("a", 3.9, "in").str_result() == " 3.9"
    assert Variable("a", 10**9, "in").str_result() == " 1000000000"


def test_str_result_with_unit():
    assert Variable("a", 0).str_result_with_unit() == " 0 \ \mathrm{}"
    assert Variable("a", 3.9, "in").str_result_with_unit() == " 3.9 \ \mathrm{in}"
    assert (
        Variable("a", 10**9, "m^2").str_result_with_unit()
        == " 1000000000 \ \mathrm{m^2}"
    )


def test_str_symbolic():
    assert Variable("a", 0).str_symbolic() == "{a}"
    assert Variable("a_2", 3.9, "in").str_symbolic() == "{a_2}"
    assert Variable("a_{ref}", 10**9, "m^2").str_symbolic() == "{a_{ref}}"


def test_str_substituted():
    assert Variable("a", 0).str_result_with_unit() == " 0 \ \mathrm{}"
    assert Variable("a", 3.9, "in").str_result_with_unit() == " 3.9 \ \mathrm{in}"
    assert (
        Variable("a", 10**9, "m^2").str_result_with_unit()
        == " 1000000000 \ \mathrm{m^2}"
    )


def test_number_format():
    assert Variable("a", 0.0000000).str_result() == " 0"
    assert Variable("a", 3.987654321, "in").str_result() == " 3.988"
    assert Variable("a", 123456789.123456, "in").str_result() == " 123456789"
