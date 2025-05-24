from pprint import pprint

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

def project_cash_flows_enhanced(
    initial_noi,
    noi_growth_rate,
    debt_service,
    hold_period=10,
    exit_cap_rate=0.05,
    selling_cost_percent=0.02,
    include_sale=True
):
    """
    Projects annual cash flows to equity with NOI growth and optional terminal sale value.
    """
    cash_flows = []
    noi = initial_noi

    for year in range(hold_period):
        annual_cash_flow = noi - debt_service
        cash_flows.append(annual_cash_flow)
        noi *= (1 + noi_growth_rate)

    if include_sale:
        final_noi = noi / (1 + noi_growth_rate)  # Adjust back one year
        terminal_value = final_noi / exit_cap_rate
        net_sale_proceeds = terminal_value * (1 - selling_cost_percent)
        cash_flows[-1] += net_sale_proceeds

    return [round(cf, 2) for cf in cash_flows]

# Example usage with enhancements
cash_flows = project_cash_flows_enhanced(
    initial_noi=600000,
    noi_growth_rate=0.02,
    debt_service=400000,
    hold_period=10,
    exit_cap_rate=0.05,
    selling_cost_percent=0.02,
    include_sale=True
)

pprint(cash_flows)
