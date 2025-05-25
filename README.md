# affordable-finance-analyzer

## Get Started
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### `inputs.py`
Summary Table
| Input Key              | What It Controls             | Main Purpose                                    |
| ---------------------- | ---------------------------- | ----------------------------------------------- |
| total_development_cost | Full capital needed          | Sets financing target                           |
| eligible_basis         | LIHTC-qualified costs        | Basis for tax credit calculation                |
| applicable_fraction    | Affordability compliance     | Adjusts qualified basis for credits             |
| credit_rate            | LIHTC % rate                 | Multiplied to basis to calculate credits        |
| soft_subsidy           | Grant or subordinate funding | Reduces amount of equity or debt required       |
| permanent_loan_rate    | Interest rate on debt        | Affects annual loan payments                    |
| permanent_loan_term    | Loan duration                | Used in amortization calculations (future step) |
| dscr_required          | Lender risk buffer           | Impacts how large your loan can be              |
| noi_year_1             | Initial cash flow            | Drives debt service and cash flow to equity     |

**Breakdown of the different fields(inputs)**:

#### `total_development_costs` (**Total cost to complete the project**):

Includes:
- Land acquisition
- Hard costs (construction)
- Soft costs (architects, lawyers, consultants)
- Developer fees
- Financing costs

Source:
- Project pro forma or budget (developer or architect)
- Cost estimator
- Previous projects
- Regional cost databases (e.g., RSMeans, HUD)

#### `eligible_basis`:

The portion of the development cost that is **eligible for LIHTC (Low-Income Housing Tax Credit)**. Not all costs are eligible - for example, land is excluded.

Formula: `Eligible Basis = Total Project Cost - Land - Ineligible Costs`

Source:
- LIHTC compliance guides from [Novogradac](https://www.novoco.com/) or [IRS](https://www.irs.gov/)
- LIHTC consultant or syndicator


#### `applicable_fraction`:

The smaller of:
- The proportion of residential units that are rent-restricted and income-qualified
- The proportion of square footage that is rent-restricted and income-qualified

Example:
- If 100% of units are affordable and qualified -> fraction = 1.0
- If only 75% are qualified -> fraction = 0.75

Source:
- Developer's affordability plan
- LIHTC application
- Rent restriction schedule


#### `credit_rate`:

The **LIHTC percentage** used to calculate annual tax credits from the eligible basis:
- 9% credit -> used for new construction or substantial rehab **without tax-exempt bonds**
- 4% credit -> used **with tax-exempt bonds**

Rates are often fixed by the IRS, but this may be "floated" if not locked.

Source:
- IRS published rates: [IRS Revenue Rulings](https://www.irs.gov/pub/irs-drop/)
- Developer's application to the Housing Finance Agency (HFA)


#### `soft_subsidy`:

**Non-repayable or low-interest funding** sources, including:
- HOME funds
- CDBG (Community Development Block Grants)
- State/Local housing trust funds
- Deferred developer fees

Used to reduce the gap between project cost and what can be financed with debt/equity.

Source:
- Municipal or state housing agencies
- Federal programs (HUD, Treasury)
- Local government RFPs or NOFAs (Notices of Funding Availability)


#### `permanent_load_rate`:

The **interest rate** on your permanent mortgage loan, typically fixed. This rate affects your annual **debt service** (loan payments).

Source:
- Term sheets from lenders (banks, CDFIs, housing finance agencies)
- Prevailing market rates (e.g., Freddie Mac Targeted Affordable)


#### `permanent_load_term`:

The **length of the mortgage**, usually in years. 30 years is standard for affordable housing projects.

This affects amortization -> longer terms = lower payments, but more interest.

Source:
- Lender underwriting guides
- State QAP (Qualified Allocation Plan) if it mandates max terms


#### `dscr_required`:

**Debt Service Coverage Ratio** is: `DSCR = Net Operating Income / Debt Service`

Lenders typically require:
- DSCR >= 1.15 for affordable housing
- DSCR >= 1.25 for conventional real estate

A higher DSCR = more cushion to make debt payments.

Source:
- Lender underwriting requirements
- State housing finance agency rules


#### `noi_year_1`:

**Net Operating Income (NOI)** is the property's income after subtracting operating expenses but **before debt service and taxes**.

This is the key metric for:
- Loan sizing
- Debt coverage
- Project profitability

Source:
- Developer's pro forma
- Comparable property operating statements
- Property manager forecasts