"""
Matpoltlib's default backend on macOS is often set to MacOSX,
which tries to use GUI-based rendering (NSWindow) -- not
allowed in a background web server process.

To avoid a chart rendering issue, we'll set the backend manually
to a non-interactive, file-based backend called "Agg" (commonly
used for server-side plotting).
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_cash_flows(cash_flows, save_path):
    years = np.arange(1, len(cash_flows) + 1)
    plt.figure()
    plt.bar(years, cash_flows, color='skyblue')
    plt.title("Annual Cash Flows to Equity")
    plt.xlabel("Year")
    plt.ylabel("Cash Flow ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_irr_curve(cash_flows, equity_investment, save_path):
    discount_rates = np.linspace(0.01, 0.3, 100)
    npvs = []

    for r in discount_rates:
        npv = -equity_investment + sum(cf / (1 + r) ** i for i, cf in enumerate(cash_flows, 1))
        npvs.append(npv)

    plt.figure()
    plt.plot(discount_rates * 100, npvs)
    plt.axhline(0, color='red', linestyle='--')
    plt.title("IRR Sensitivity Curve")
    plt.xlabel("Discount Rate (%)")
    plt.ylabel("Net Present Value ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_capital_stack(capital_stack, save_path):
    labels = []
    values = []

    for k, v in capital_stack.items():
        if isinstance(v, (int, float)) and v > 0 and "Total" not in k:
            labels.append(k)
            values.append(v)
        elif isinstance(v, (dict)):
            labels.append(k)
            sum = 0
            for key, val in v.items():
                if isinstance(val, (int, float)) and val > 0:
                    sum += val
            values.append(sum)
    
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Capital Stack Distribution")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()