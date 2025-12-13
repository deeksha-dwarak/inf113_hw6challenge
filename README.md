# Proof-of-Concept Challenge: Securing a Legacy Invoice Import Service

## Codesafe Context
This repository contains a **proof-of-concept security challenge for the Codesafe platform**.  
The challenge is designed to help learners practice software enginneering concepts by identifying and fixing a real-world vulnerability in Python code! :) 

## Narrative (User Story)

I want to identify and patch an 'eval()' -based injection vulnerability in a legacy service,  
so that I can learn how to securely process untrusted input without breaking existing functionality.

## Scenario
You are onboarding as a junior software engineer (congrats btw) on a team that maintains a legacy invoice import service! External partners submit invoice totals to your system using:

- Roman numerals (e.g., 'XXII')
- Simple arithmetic expressions combining Roman numerals and integers (e.g., "X + I", "XXI + 3", "10 - IV" )

A previous developer implemented this quickly by converting Roman numerals to integers and then calling Python’s existing 'eval()' to compute the result.

Although the system appears to work, this design introduced a serious liability!!! Attackers can craft inputs that attempt to execute arbitrary code or access Python internals.
(Insert dramatic sound affect here)

------------------------

## Your Task
You are given starter source code that:
- Is functional
- Exceeds 100 lines of code
- Contains an intentional security flaw ('eval()' on user-derived input)

Your task is to update the function:

**compute_invoice_total(expr: str) -> int**

so that it:

1. Removes the use of eval()
2. Safely parses and evaluates expressions containing only:
   - Roman numerals I V X L C D M
   - Integers
   - Operators + and -
   - Whitespace
3. Rejects all other input, including:
   - Parentheses
   - Additional operators (*, /)
   - Code execution attempts
4. Rejects malformed expressions, such as:
   - Consecutive operators (X + + V)
   - Expressions starting or ending with an operator
5. Includes basic input hardening by rejecting excessively large expressions

---

## Starter Code
- Located in `starter_code/app.py`
- Contains existing functionality for:
  - Roman numeral conversion
  - Expression parsing
- Intentionally insecure for educational purposes

---

## Test Cases
- Located in `tests/test_app.py`
- Verify:
  - Correct behavior for valid inputs
  - Rejection of malicious, malformed, or unsupported inputs
- Serve as the validation mechanism for completing the challenge

---

## Intended Solution
- Located in `solution/app_secure.py`
- Demonstrates a correct and secure implementation
- Passes all provided test cases
- Used by graders for evaluation

---

## Educational Value
This challenge supports Codesafe’s product goals by:
- Teaching secure input
