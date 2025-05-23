import numpy_financial as npf

def calculate_irr(cash_flows, equity_investment):
    full_flows = [-equity_investment] + cash_flows
    return round(npf.irr(full_flows) * 100, 2)

def calculate_dscr(noi, debt_service):
    return round(noi / debt_service, 2)