def calculate_lihtc_equity(eligible_basis, applicable_fraction, credit_rate, term=10, pricing=0.90):
    annual_credit = eligible_basis * applicable_fraction * credit_rate
    total_credit = annual_credit * term
    equity = total_credit * pricing
    return round(equity, 2)