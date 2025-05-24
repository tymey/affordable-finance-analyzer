from inputs import get_project_inputs
from lihtc_calculator import calculate_lihtc_equity_extended
from capital_stack import build_advanced_capital_stack
from cashflow_model import project_cash_flows_enhanced
from utils import calculate_irr, calculate_dscr

def main():
    # 1. Gather user-defined assumptions
    inputs = get_project_inputs()

    # 2. Calculate LIHTC equity and disbursement
    lihtc_info = calculate_lihtc_equity_extended(
        eligible_basis=inputs["eligible_basis"],
        applicable_fraction=inputs["applicable_fraction"],
        credit_rate=inputs["credit_rate"],
        pricing=inputs["pricing"],
        credit_type=inputs["credit_type"],
        include_syndication_fee=inputs["include_syndication_fee"],
        syndication_fee_percent=inputs["syndication_fee_percent"],
        use_bridge_loan=inputs["use_bridge_loan"],
        bridge_loan_interest=inputs["bridge_loan_interest"],
        bridge_loan_term_years=inputs["bridge_loan_term_years"]
    )

    # 3. Build full capital stack using LIHTC equity
    capital_stack = build_advanced_capital_stack(inputs, lihtc_info["Net Equity After Fees"])

    # 4. Project 10-year cash flows
    cash_flows = project_cash_flows_enhanced(
        initial_noi=inputs["noi_year_1"],
        noi_growth_rate=inputs["noi_growth_rate"],
        debt_service=capital_stack["Loan (DSCR & LTV Constrained)"] * inputs["permanent_loan_rate"],
        hold_period=inputs["hold_period"],
        exit_cap_rate=inputs["exit_cap_rate"],
        selling_cost_percent=inputs["selling_cost_percent"],
        include_sale=True
    )

    # 5. Calculate IRR and DSCR
    irr = calculate_irr(cash_flows, equity_investment=capital_stack["Equity Required"])
    dscr = calculate_dscr(inputs["noi_year_1"], capital_stack["Loan (DSCR & LTV Constrained)"] * inputs["permanent_loan_rate"])

    # 6. Print Results
    print("\nCapital Stack:")
    for k, v in capital_stack.items():
        print(f"{k}: ${v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}")

    print("\nFinancial Metrics:")
    print(f"IRR: {irr}%")
    print(f"DSCR (Year 1): {dscr}")

    print("\nLIHTC Equity Disbursement Schedule:")
    for k, v in lihtc_info["Disbursement Schedule"].items():
        print(f"{k}: ${v:,.2f}")

    print("\nCash Flows to Equity:")
    for i, cf in enumerate(cash_flows, 1):
        print(f"Year {i}: ${cf:,.2f}")

if __name__ == "__main__":
    main()
