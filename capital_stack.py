def build_capital_stack(inputs, lihtc_equity):
    gap = inputs["total_development_cost"] - (lihtc_equity + inputs["soft_subsidy"])
    loan = min(gap, 0.75 * inputs["total_development_cost"]) # LTV Rule of Thumb
    equity = inputs["total_development_cost"] - (lihtc_equity + inputs["soft_subsidy"] + loan)
    return {
        "LIHTC Equity": lihtc_equity,
        "Soft Subsidy": inputs["soft_subsidy"],
        "Loan": loan,
        "Equity": equity,
    }