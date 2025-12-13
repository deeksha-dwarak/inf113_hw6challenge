"""
Legacy Invoice Import Service (STARTER CODE - INTENTIONALLY INSECURE!!!)
"""

class InvoiceFormatError(ValueError):
    """Raised when an invoice expression cannot be processed."""


def compute_invoice_total(expr: str) -> int:
    """
    INTENTIONALLY INSECURE STARTER IMPLEMENTATION.

    This function uses eval() on untrusted input.
    Learners must remove eval() and implement safe parsing.
    """
    if not isinstance(expr, str):
        raise InvoiceFormatError("Expression must be a string")

    try:
        return eval(expr)
    except Exception:
        raise InvoiceFormatError("Invalid invoice expression")
