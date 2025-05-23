from inputs import get_project_inputs
from lihtc_calculator import calculate_lihtc_equity
from capital_stack import build_capital_stack
from cashflow_model import project_cash_flows
from utils import calculate_irr, calculate_dscr

def main():
    inputs = get_project_inputs()
    lihtc_equity = calculate_lihtc_equity(
        inputs["eligible_basis"],
        inputs["applicable_fraction"],
        inputs["credit_rate"],
    )
    capital = build_capital_stack(inputs, lihtc_equity)

    debt_service = capital["Loan"] * inputs["permanent_loan_rate"]
    cash_flows = project_cash_flows(inputs["noi_year_1"], debt_service)
    irr = calculate_irr(cash_flows, capital["Equity"])
    dscr = calculate_dscr(inputs["noi_year_1"], debt_service)

    print("\n Capital Stack:")
    for k, v in capital.items():
        print(f"{k}: ${v:,.2f}")
    
    print(f"\n IRR: {irr}%")
    print(f"\n DSCR: {dscr}")

if __name__ == "__main__":
    main()