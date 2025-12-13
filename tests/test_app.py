import pytest

from starter_code.app import compute_invoice_total, InvoiceFormatError


# -------------------------
# Functionality tests (must pass after patch)
# -------------------------

def test_roman_only_examples():
    assert compute_invoice_total("III") == 3
    assert compute_invoice_total("LVIII") == 58
    assert compute_invoice_total("MCMXCIV") == 1994


def test_mixed_expression_plus_minus():
    assert compute_invoice_total("X + V + 3") == 18
    assert compute_invoice_total("10 - IV") == 6
    assert compute_invoice_total("  X+V+3  ") == 18


def test_edge_valid_cases():
    assert compute_invoice_total("I") == 1
    assert compute_invoice_total("MMMCMXCIX") == 3999  # max valid roman numeral


# -------------------------
# Security rejection tests
# These should FAIL on the eval-based starter code and PASS after patch.
# -------------------------

def test_reject_code_injection_strings():
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("__import__('os').system('echo pwned')")

    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + __import__('os').system('echo pwned')")


def test_reject_disallowed_characters_and_operators():
    # Parentheses not allowed
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + (V)")

    # Only + and - are allowed; * is not allowed
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + V * 3")

    # Semicolons not allowed
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + V; 3")

    # Division not allowed
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + V / 3")


# -------------------------
# Grammar safety tests
# -------------------------

def test_reject_malformed_operator_sequences():
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X + + V")

    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("+ X")

    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("X -")


def test_reject_empty_or_whitespace_only():
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("")

    with pytest.raises(InvoiceFormatError):
        compute_invoice_total("   ")


# -------------------------
# Abuse / size limit tests
# -------------------------

def test_reject_excessive_size():
    # Very long expression should be rejected by hardening checks
    long_expr = " + ".join(["I"] * 2000)
    with pytest.raises(InvoiceFormatError):
        compute_invoice_total(long_expr)

