def project_cash_flows(noi, debt_service, hold_period=10):
    cash_flows = [-debt_service] * hold_period
    for i in range(hold_period):
        cash_flows[i] = noi - debt_service
    return cash_flows