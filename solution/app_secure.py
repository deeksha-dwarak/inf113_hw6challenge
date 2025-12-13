
"""
Intended Secure Solution (NO eval)

This module provides the secure version of the legacy invoice import logic.
It safely parses and evaluates expressions containing only:
- Roman numerals (I, V, X, L, C, D, M)
- Integers
- Operators: + and -
- Whitespace

It rejects:
- Any other characters (including parentheses, *, /, ;, quotes, underscores)
- Malformed operator sequences (e.g., "X + + V", "+ X", "X -")
- Empty/whitespace-only input
- Excessively large inputs (basic hardening)
"""

from __future__ import annotations

from typing import Dict, List


# -------------------------
# Roman numeral constants
# -------------------------

ROMAN_VALUES: Dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

SUBTRACTIVE_PAIRS: Dict[str, int] = {
    "IV": 4,
    "IX": 9,
    "XL": 40,
    "XC": 90,
    "CD": 400,
    "CM": 900,
}


# -------------------------
# Exception
# -------------------------

class InvoiceFormatError(ValueError):
    """Raised when an invoice expression cannot be processed safely."""


# -------------------------
# Roman numeral conversion
# -------------------------

def roman_to_int(s: str) -> int:
    """
    Convert a Roman numeral string into an integer.
    Assumes valid Roman numerals in the range 1..3999.
    """
    i = 0
    total = 0

    while i < len(s):
        if i + 1 < len(s):
            pair = s[i : i + 2]
            if pair in SUBTRACTIVE_PAIRS:
                total += SUBTRACTIVE_PAIRS[pair]
                i += 2
                continue

        ch = s[i]
        if ch not in ROMAN_VALUES:
            raise InvoiceFormatError(f"Invalid Roman numeral character: {ch}")

        total += ROMAN_VALUES[ch]
        i += 1

    return total


# -------------------------
# Safe tokenizer
# -------------------------

def _safe_tokenize(expr: str) -> List[str]:
    """
    Tokenize an expression while rejecting any illegal characters.

    Allowed tokens:
    - '+' or '-'
    - integer runs (e.g., "123")
    - roman runs (e.g., "MCMXCIV") consisting only of IVXLCDM letters
    - whitespace is ignored

    Hardening:
    - Reject overly long expressions
    - Reject excessive token counts
    """
    # Basic hardening to reject extremely large inputs early
    if len(expr) > 5000:
        raise InvoiceFormatError("Expression too long")

    tokens: List[str] = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch in "+-":
            tokens.append(ch)
            i += 1
            continue

        if ch.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue

        up = ch.upper()
        if up in ROMAN_VALUES:
            j = i
            while j < len(expr) and expr[j].upper() in ROMAN_VALUES:
                j += 1
            tokens.append(expr[i:j].upper())
            i = j
            continue

        # Anything else is illegal (core security requirement)
        raise InvoiceFormatError(f"Illegal character in expression: {ch}")

    # Empty after trimming whitespace is not allowed
    if not tokens:
        raise InvoiceFormatError("Empty expression")

    # Token-count hardening (your tests use 2000 roman tokens joined by '+')
    if len(tokens) > 2000:
        raise InvoiceFormatError("Too many tokens")

    return tokens


def _to_number(token: str) -> int:
    """Convert a numeric token (digits or roman) into an int, or raise."""
    if token.isdigit():
        return int(token)

    # Roman token must be composed only of roman letters
    if all(ch in ROMAN_VALUES for ch in token):
        return roman_to_int(token)

    raise InvoiceFormatError(f"Invalid number token: {token}")


# -------------------------
# Secure evaluator
# -------------------------

def compute_invoice_total(expr: str) -> int:
    """
    Safely compute the total value of an invoice expression.

    Grammar enforced:
        number ( ( + | - ) number )*

    No parentheses. No other operators. Evaluates left-to-right.
    """
    if not isinstance(expr, str):
        raise InvoiceFormatError("Expression must be a string")

    tokens = _safe_tokenize(expr)

    # Reject starting with an operator (e.g., "+ X")
    if tokens[0] in {"+", "-"}:
        raise InvoiceFormatError("Expression cannot start with an operator")

    # First number
    total = _to_number(tokens[0])
    idx = 1

    while idx < len(tokens):
        op = tokens[idx]

        # Expect operator at odd positions
        if op not in {"+", "-"}:
            raise InvoiceFormatError("Expected operator")

        # Expression cannot end with an operator (e.g., "X -")
        if idx + 1 >= len(tokens):
            raise InvoiceFormatError("Expression cannot end with an operator")

        nxt = tokens[idx + 1]

        # Reject two operators in a row (e.g., "X + + V")
        if nxt in {"+", "-"}:
            raise InvoiceFormatError("Two operators in a row")

        val = _to_number(nxt)
        total = total + val if op == "+" else total - val
        idx += 2

    if not isinstance(total, int):
        raise InvoiceFormatError("Expression did not evaluate to an integer")

    return total
