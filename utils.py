import numpy_financial as npf

"""
These functions provide metrics, like IRR and DSCR, that investors
and lenders rely on to assess deal performance and risk.
"""

"""
IRR (Internal Rate of Return) is the discount rate that makes the
Net Present Value (NPV) of all cash flows = 0.

It accounts for:
    - Time value of money
    - Initial outlay
    - Annual income or losses
"""
def calculate_irr(cash_flows, equity_investment):
    # Prepends the initial equity investment (negative) to the list of future positive cash flows.
    full_flows = [-equity_investment] + cash_flows
    # Calculate IRR and express it as a percentage
    return round(npf.irr(full_flows) * 100, 2)

"""
DSCR = Debt Service Coverage Ratio
Formula
    - DSCR = Net Operating Income / Annual Debt Payment

Interpreted as:
    - 1.0 = break-even
    - >1.15 = healthy buffer (typical lender minimum)
    - < 1.0 = cannot cover debt - red flag
"""
def calculate_dscr(noi, debt_service):
    return round(noi / debt_service, 2)