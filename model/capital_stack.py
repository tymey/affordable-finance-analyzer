from pprint import pprint

"""
This function is used to construct the financing structure (a.k.a. capital stack)
for a real estate development project.

This is a critical step in evaluating whether a project is feasible and financeable.
"""

def build_capital_stack(inputs, lihtc_equity):
    gap = inputs["total_development_cost"] - (lihtc_equity + inputs["soft_subsidy"])
    loan = min(gap, 0.75 * inputs["total_development_cost"]) # LTV Rule of Thumb
    equity = inputs["total_development_cost"] - (lihtc_equity + inputs["soft_subsidy"] + loan)
    return {
        "LIHTC Equity": lihtc_equity,
        "Soft Subsidy": inputs["soft_subsidy"],
        "Loan": loan,
        "Equity": equity,
    }

"""
Gap:
The remaining funding gap after applying:
    - LIHTC equity raised (from lihtc_calculator.py)
    - Soft subsidies (HOME, CDBG, etc.)
This gap must be filled by a loan and/or developer equity.

Loan:
We assume the project can borrow up to 75% of the total cost, a common underwriting limit used by lenders to manage risk.
We then cap the load at the smaller of:
    - The remaining gap
    - 75% of total development cost
This protects against over leveraging, which could cause the DSCR to fall below acceptable levels.

Equity:
Whatever isn't covered by tax credits, soft funding, or a loan must be covered by developer equity - the riskiest and most expensive source of capital
Equity is usually provided by:
    - The developer
    - Equity investors (non-LIHTC)
    - A related-party entity
This line of code ensures we balance the sources and uses.


Why This Is Important:
Building a strong capital stack is essential for:
    - Balancing risk and return
    - Qualifying for financing (lenders want acceptable DSCR, investors want strong IRR)
    - Satisfying government funding layers (each with their own rules)
The function above is a simplified version - in real development, you'd also model:
    - Mezzanine debt
    - Deferred developer fee
    - Tax-exempt bond proceeds
    - Bridge loan proceeds
"""

def build_advanced_capital_stack(inputs, lihtc_equity):
    """
    Enhanced capital stack builder with:
    - DSCR-based loan sizing
    - Interest reserve for loan
    - Multiple soft subsidy sources
    - Deferred developer fee placeholder
    """

    # Aggregate soft subsidies
    soft_subsidies = sum(inputs.get("soft_subsidies", {}).values())

    # DSCR-based maximum loan sizing
    noi = inputs["noi_year_1"]
    required_dscr = inputs["dscr_required"]
    annual_debt_service_capacity = noi / required_dscr
    loan_interest_rate = inputs["permanent_loan_rate"]
    loan_term_years = inputs["permanent_loan_term"]

    # Use annuity formula to estimate max loan amount based on DSCR
    # Formula: loan = (Debt service * (1 - (1 + r)^-n)) / r
    r = loan_interest_rate
    n = loan_term_years
    loan_limit_by_dscr = annual_debt_service_capacity * ((1 - (1 + r) ** -n) / r)

    # Cap loan by 75% LTV as well
    loan_limit_by_ltv = 0.75 * inputs["total_development_cost"]
    loan = min(loan_limit_by_dscr, loan_limit_by_ltv)

    # Interest reserve for construction period (e.g., 2 years)
    interest_reserve = loan * loan_interest_rate * inputs.get("construction_period_years", 2)

    # Total sources so far
    used_sources = lihtc_equity + soft_subsidies + loan

    # Remaining need is filled with developer equity and deferred dev fee (placeholder)
    funding_gap = inputs["total_development_cost"] + interest_reserve - used_sources
    deferred_dev_fee = min(funding_gap, inputs.get("max_deferred_dev_fee", 500000))
    equity = funding_gap - deferred_dev_fee

    return {
        "LIHTC Equity": round(lihtc_equity, 2),
        "Soft Subsidies": {k: round(v, 2) for k, v in inputs.get("soft_subsidies", {}).items()},
        "Loan (DSCR & LTV Constrained)": round(loan, 2),
        "Interest Reserve": round(interest_reserve, 2),
        "Deferred Developer Fee": round(deferred_dev_fee, 2),
        "Equity Required": round(equity, 2),
        "Total Sources": round(used_sources + interest_reserve + deferred_dev_fee + equity, 2),
        "Total Uses": round(inputs["total_development_cost"] + interest_reserve, 2)
    }

# Example inputs for enhanced capital stack
inputs_example = {
    "total_development_cost": 12000000,
    "soft_subsidies": {
        "HOME": 1000000,
        "CDBG": 750000
    },
    "permanent_loan_rate": 0.05,
    "permanent_loan_term": 30,
    "construction_period_years": 2,
    "dscr_required": 1.15,
    "noi_year_1": 600000,
    "max_deferred_dev_fee": 500000
}

# Assume LIHTC equity calculated earlier
lihtc_equity_example = 8000000

# pprint(build_advanced_capital_stack(inputs_example, lihtc_equity_example))
