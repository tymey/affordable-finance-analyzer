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