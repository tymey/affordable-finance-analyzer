"""
This function simulates yearly cash flows to equity investors
over a set holding period by subtracting loan payments (debt service)
Net Operating Income (NOI).
"""

def project_cash_flows(noi, debt_service, hold_period=10):
    cash_flows = [-debt_service] * hold_period
    for i in range(hold_period):
        cash_flows[i] = noi - debt_service
    return cash_flows

"""
cash_flows:
    - Creates a list of debt payments with initial negative values to start with.
    - Example for 3-year hold: [-300000, -300000, -300000]

for-loop:
    - Loop over each year in the hold period (e.g., 10 years)
    - Replaces each year's cash flow with NOI minus debt service, which is the net cash flow to equity
    - NOI = income after expenses, before financing
    - Debt service = principal + interest paid annually
"""