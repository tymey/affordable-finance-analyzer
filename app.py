import os
from flask import Flask, render_template, request, send_file
from model.inputs import get_project_inputs
from model.lihtc_calculator import calculate_lihtc_equity_extended
from model.capital_stack import build_advanced_capital_stack
from model.cashflow_model import project_cash_flows_enhanced
from model.utils import calculate_irr, calculate_dscr
from model.report_generator import generate_excel_report, generate_pdf_report
from model.chart_generator import plot_cash_flows, plot_irr_curve, plot_capital_stack

# Temporary files
EXCEL_PATH = "outputs/report.xlsx"
PDF_PATH = "outputs/report.pdf"

# Chart Directory
CHART_DIR = "static/charts"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # For now, use static inputs
        inputs = get_project_inputs()

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

        capital_stack = build_advanced_capital_stack(inputs, lihtc_info["Net Equity After Fees"])

        cash_flows = project_cash_flows_enhanced(
            initial_noi=inputs["noi_year_1"],
            noi_growth_rate=inputs["noi_growth_rate"],
            debt_service=capital_stack["Loan (DSCR & LTV Constrained)"] * inputs["permanent_loan_rate"],
            hold_period=inputs["hold_period"],
            exit_cap_rate=inputs["exit_cap_rate"],
            selling_cost_percent=inputs["selling_cost_percent"],
            include_sale=True
        )

        irr = calculate_irr(cash_flows, capital_stack["Equity Required"])
        dscr = calculate_dscr(inputs["noi_year_1"], capital_stack["Loan (DSCR & LTV Constrained)"] * inputs["permanent_loan_rate"])

        # Generate reports
        generate_excel_report(capital_stack, lihtc_info, cash_flows, irr, dscr, EXCEL_PATH)
        generate_pdf_report(capital_stack, lihtc_info, cash_flows, irr, dscr, PDF_PATH)

        # Generate charts
        os.makedirs(CHART_DIR, exist_ok=True)

        cf_chart = os.path.join(CHART_DIR, "cash_flows.png")
        irr_chart = os.path.join(CHART_DIR, "irr_curve.png")
        stack_chart = os.path.join(CHART_DIR, "capital_stack.png")

        plot_cash_flows(cash_flows, cf_chart)
        plot_irr_curve(cash_flows, capital_stack["Equity Required"], irr_chart)
        plot_capital_stack(capital_stack, stack_chart)

        return render_template("results.html",
                               capital_stack=capital_stack,
                               cash_flows=cash_flows,
                               irr=irr,
                               dscr=dscr,
                               lihtc_info=lihtc_info,
                               cf_chart=cf_chart,
                               irr_chart=irr_chart,
                               stack_chart=stack_chart)

    return render_template("index.html")

@app.route("/download/excel")
def download_excel():
    return send_file(EXCEL_PATH, as_attachment=True)

@app.route("/download/pdf")
def download_pdf():
    return send_file(PDF_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
