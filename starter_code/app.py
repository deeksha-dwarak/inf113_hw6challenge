"""
Legacy Invoice Import Service (STARTER CODE - INTENTIONALLY INSECURE!!!)

This module processes invoice totals submitted by external partners.
Inputs may contain:
- Roman numerals (I, V, X, L, C, D, M)
- Integers
- Simple arithmetic using + and -

SECURITY WARNING:
This starter version uses eval() on user-derived input.
Learners are expected to remove eval() and implement safe parsing.
"""
import json
import sys
import time 
from dataclasses import dataclass

from __future__ import annotations

from dataclasses import dataclass
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
# Exceptions / data models
# -------------------------

class InvoiceFormatError(ValueError):
    """Raised when an invoice expression cannot be processed."""


@dataclass
class InvoiceResult:
    original: str
    normalized: str
    total: int
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
        # Handle subtractive pairs first (e.g., IV, IX)
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
# Tokenization / normalization
# -------------------------

def _tokenize(expr: str) -> List[str]:
    """
    Break an expression into tokens.
    This is intentionally permissive to illustrate a security issue.
    """
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

        if ch.upper() in ROMAN_VALUES:
            j = i
            while j < len(expr) and expr[j].upper() in ROMAN_VALUES:
                j += 1
            tokens.append(expr[i:j].upper())
            i = j
            continue

        # Any other character is passed through (unsafe)
        tokens.append(ch)
        i += 1

    return tokens


def _normalize_tokens(toke

