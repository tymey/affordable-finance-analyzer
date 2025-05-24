from pprint import pprint # Pretty printing for objects

"""
This function is used to estimate how much equity a developer can raise using
Low-Income Housing Tax Credits (LIHTC) - specifically the 9% credit.

This function calculates how much LIHTC equity a developer can raise
by selling tax credits to investors, based on:
    1. The eligible development costs
    2. The percentage of affordable units
    3. The IRS credit rate
    4. The credit term (usually 10 years)
    5. What investors are willing to pay per dollar of credit ("pricing")
"""

def calculate_lihtc_equity(eligible_basis, applicable_fraction, credit_rate, term=10, pricing=0.90):
    # (eligible_basis * applicable_fraction) = qualified_basis
    annual_credit = eligible_basis * applicable_fraction * credit_rate
    total_credit = annual_credit * term
    equity = total_credit * pricing
    # Rounds the equity result to two decimal places to make it cleaner for reporting
    return round(equity, 2)

"""
Qualified Basis = Eligible Basis * Applicable Fraction
    - The portion of the development cost that can generate tax credits.
    - Eligible Basis: Total costs that qualify under LIHTC rules (e.g., construction costs, but not land)
    - Applicable Fraction: The smaller of:
        - % of units that are income-qualified
        - % of floor area that is income-qualified

Credit Rate:
    - 9% for new construction or substantial rehab (without bonds)
    - 4% if tax-exempt bonds are used

Annual Tax Credit:
    - The annual amount of tax credits for the project
    - Example: $10,000,000 qualified basis * 9% = $900,000 per year in tax credits

Total Tax Credits = Annual Tax Credit * Terms
    - The total credits awarded over 10 years (number of terms).
    - This is how long the IRS distributes the credits (unless it's a stepped-up front-loading structure, which is rare).
    - The term is always 10 years under standard LIHTC programs

Equity = Total Tax Credits * Pricing
    - This converts the dollar value of tax credits into the equity a developer receives from investors (e.g., syndicators or LIHTC equity funds).
    - "Pricing" is what investors are willing to pay per $1 of tax credit
    - Typical pricing ranges:
        - $0.85-$0.95 per dollar for 9% LIHTCs
        - $0.80-$0.90 for 4% credits

Real-World Considerations:
    - The function assumes full credit delivery (no shortfall or delays).
    - It doesn't include adjuster clauses (used if projects miss delivery timelines).
    - We might want to model equity contributions over time, example:
        - 25% at closing
        - 50% at construction completion
        - 25% at stabilization
    - We can expand this to model 4% LIHTC with bonds, syndication fees, or bridge loan financing based on the equity raise.
"""

"""
Possible Extension:

This model reflects the real-world cash flow challenges in LIHTC deals:
    - Credits are paid out slowly, while construction needs capital upfront
    - Syndicators charge fees that reduce usable equity
    - Developers often need short-term bridge loans, increasing cost and risk.
"""
def calculate_lihtc_equity_extended(
    eligible_basis: float,
    applicable_fraction: float,
    credit_rate: float,
    term: int = 10,
    pricing: float = 0.90,
    credit_type: str = "9%",
    include_syndication_fee: bool = True,
    syndication_fee_percent: float = 0.05,
    use_bridge_loan: bool = True,
    bridge_loan_interest: float = 0.06,
    bridge_loan_term_years: int = 2
):
    qualified_basis = eligible_basis * applicable_fraction
    annual_credit = qualified_basis * credit_rate
    total_credit = annual_credit * term
    gross_equity = total_credit * pricing

    # Syndication fee
    syndication_fee = gross_equity * syndication_fee_percent if include_syndication_fee else 0
    net_equity = gross_equity - syndication_fee

    # Disbursement schedule (assumes: 25% at closing, 50% during construction, 25% at stabilization)
    disbursement_schedule = {
        "Closing": round(net_equity * 0.25, 2),
        "Construction Completion": round(net_equity * 0.50, 2),
        "Stabilization": round(net_equity * 0.25, 2),
    }

    # Bridge loan if equity not paid upfront
    bridge_loan = {}
    if use_bridge_loan:
        average_equity_gap = net_equity * (0.75 / 2)  # 75% paid after closing, so average over 2 years
        interest_due = average_equity_gap * bridge_loan_interest * bridge_loan_term_years
        bridge_loan = {
            "Bridge Loan Principal Needed": round(average_equity_gap, 2),
            "Interest Over Term": round(interest_due, 2),
            "Total Repayment": round(average_equity_gap + interest_due, 2)
        }

    return {
        "Credit Type": credit_type,
        "Qualified Basis": qualified_basis,
        "Annual Credit": round(annual_credit, 2),
        "Total Credits (10 years)": round(total_credit, 2),
        "Investor Pricing": pricing,
        "Gross Equity Raised": round(gross_equity, 2),
        "Syndication Fee": round(syndication_fee, 2),
        "Net Equity After Fees": round(net_equity, 2),
        "Disbursement Schedule": disbursement_schedule,
        "Bridge Loan (if used)": bridge_loan
    }

# Run an example with extended modeling
# pprint(calculate_lihtc_equity_extended(
#     eligible_basis=10_000_000,
#     applicable_fraction=1.0,
#     credit_rate=0.09,
#     pricing=0.90,
#     credit_type="9%",
#     include_syndication_fee=True,
#     syndication_fee_percent=0.05,
#     use_bridge_loan=True,
#     bridge_loan_interest=0.06,
#     bridge_loan_term_years=2
# ))
