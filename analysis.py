"""
Business analysis logic: financial ratios, marketing metrics, and AI report generation.
"""

import json
from llm_client import call_llm


def construct_prompt_financial(results: dict) -> str:
    """Generate CFO-style financial analysis from ratio data."""
    prompt = f"""You are a Senior Strategic Business Consultant and Fractional CFO. I am going to provide you with a JSON object containing the financial ratios of my business.

Your Task:

Executive Summary: Give me a 3-sentence 'vibe check' on the company's health.

The Red Flags: Identify any ratios that suggest liquidity, solvency, or efficiency risks.

The Green Flags: What are we doing exceptionally well?

Operational Advice: Based on the 'Operational' and 'DuPont' sections, give me 3 actionable steps to improve profitability or cash flow.

Benchmark Comparison: Compare these to standard healthy industry benchmarks (assume a general mid-market manufacturing/retail context).

The Data: {json.dumps(results, indent=2)}"""
    return call_llm(prompt)


def construct_prompt_marketing(results: dict) -> str:
    """Generate CMO-style marketing analysis from unit economics data."""
    prompt = f"""You are a data-driven Chief Marketing Officer (CMO) with a background in Growth Engineering and Unit Economics.

Task: Analyze the provided Marketing & Customer Acquisition data and provide a high-level strategic evaluation.

Please structure your response as follows:

The Efficiency Score: On a scale of 1-10, how healthy is this growth engine? (Base this heavily on the LTV:CAC and Payback Period).

Growth vs. Burn: Are we spending too much to acquire customers, or are we being too conservative?

The Leaking Bucket Check: Analyze the Churn and Retention metrics. Is our growth sustainable, or are we losing customers too fast to keep the "bucket" full?

CMO Recommendations: Provide 3 specific strategies to either:
- Optimize CAC (if the payback period is too long).
- Increase LTV (if the margin or retention is low).
- Scale Spend (if the LTV:CAC is >3 and we should be "pouring gas on the fire").

Financial Alignment: Briefly explain how these marketing metrics will impact the company's "Bottom Line" Net Income over the next 6 months.

The Data for Analysis: {json.dumps(results, indent=2)}"""
    return call_llm(prompt)


def construct_prompt_ceo(financial_report: str, marketing_report: str) -> str:
    """Generate CEO synthesis from CFO and CMO reports."""
    prompt = f"""You are the CEO of a high-growth company. You are presiding over a board meeting with your CFO and CMO.

The Objective: Synthesize the Financial Report and the Marketing Report to determine the company's "True North." You need to identify if the growth strategy is sustainable or if the company is at risk.

Analysis Requirements:

The Alignment Audit: Is the Marketing department spending cash at a rate that the Balance Sheet can support? Point out any friction between Marketing Spend and Net Income/Cash Reserves.

Unit Economics vs. Overhead: The CMO reports on LTV/CAC (unit level), but the CFO reports on OpEx (company level). Are we "profitable on a unit basis" but "losing money on a GAAP basis"? Explain what this means for our runway.

The "Growth-Profitability" Seesaw: Should we:
- Aggressive Growth: Pour more cash into marketing because the LTV/CAC and ROE justify it?
- Operational Efficiency: Freeze marketing spend and focus on fixing the "clogged" inventory/assets identified by the CFO?
- Capital Raise: Is our current trajectory going to require a debt or equity raise in the next 6-12 months?

CEO Directive: Give 3 high-level directives. These should be "Orders" to your CFO and CMO to get them in sync.

CFO DATA (Financials): {financial_report}

CMO DATA (Marketing): {marketing_report}"""
    return call_llm(prompt)


def financial_analysis(
    Revenue, COGS, Gross_Profit, Sales_and_Marketing, Research_and_Development,
    General_and_Administrative, EBITDA, Depreciation_and_Amortization, EBIT,
    Interest_Expense, Net_Income, cash_equivalents, accounts_receivable,
    inventory, fixed_assets_ppe, intangible_assets, accounts_payable,
    accrued_expenses, long_term_debt, shareholders_equity,
    stock_price=0, shares_outstanding=1
) -> tuple[dict, str]:
    """
    Compute financial ratios and generate CFO AI report.
    Returns (metrics_dict, ai_report_text).
    """
    Current_Assets = cash_equivalents + accounts_receivable + inventory
    Total_Assets = Current_Assets + fixed_assets_ppe + intangible_assets
    Current_Liab = accounts_payable + accrued_expenses
    NWC = Current_Assets - Current_Liab

    current_ratio = Current_Assets / Current_Liab if Current_Liab else 0
    quick_ratio = (Current_Assets - inventory) / Current_Liab if Current_Liab else 0
    cash_ratio = cash_equivalents / Current_Liab if Current_Liab else 0
    interval_measure = Current_Assets / (COGS / 365) if COGS else 0

    total_debt_ratio = (Total_Assets - shareholders_equity) / Total_Assets if Total_Assets else 0
    equity_multiplier = Total_Assets / shareholders_equity if shareholders_equity else 0
    ltd_ratio = long_term_debt / (long_term_debt + shareholders_equity) if (long_term_debt + shareholders_equity) else 0
    tie = EBIT / Interest_Expense if Interest_Expense else 0
    cash_coverage = EBITDA / Interest_Expense if Interest_Expense else 0

    total_asset_turnover = Revenue / Total_Assets if Total_Assets else 0
    nwc_turnover = Revenue / NWC if NWC else 0
    fixed_asset_turnover = Revenue / fixed_assets_ppe if fixed_assets_ppe else 0

    gross_margin = Gross_Profit / Revenue if Revenue else 0
    profit_margin = Net_Income / Revenue if Revenue else 0
    roa = Net_Income / Total_Assets if Total_Assets else 0
    roe = Net_Income / shareholders_equity if shareholders_equity else 0

    dupont_roe = profit_margin * total_asset_turnover * equity_multiplier

    market_cap = stock_price * shares_outstanding
    pe_ratio = stock_price / (Net_Income / shares_outstanding) if Net_Income and shares_outstanding else 0
    market_to_book = market_cap / shareholders_equity if shareholders_equity else 0
    price_sales = market_cap / Revenue if Revenue else 0
    enterprise_value = market_cap + long_term_debt - cash_equivalents
    ev_ebitda = enterprise_value / EBITDA if EBITDA else 0

    inv_turnover = COGS / inventory if inventory else 0
    days_sales_inv = 365 / inv_turnover if inv_turnover else 0
    rec_turnover = Revenue / accounts_receivable if accounts_receivable else 0
    days_sales_rec = 365 / rec_turnover if rec_turnover else 0

    financial_results = {
        "Liquidity": {"Current": round(current_ratio, 2), "Quick": round(quick_ratio, 2), "Cash": round(cash_ratio, 2), "Interval": round(interval_measure, 2)},
        "Solvency": {"Debt Ratio": round(total_debt_ratio, 2), "Multiplier": round(equity_multiplier, 2), "LTD": round(ltd_ratio, 2), "TIE": round(tie, 2), "Cash Coverage": round(cash_coverage, 2)},
        "Turnover": {"Total Asset": round(total_asset_turnover, 2), "NWC": round(nwc_turnover, 2), "Fixed Asset": round(fixed_asset_turnover, 2)},
        "Profitability": {"Gross Margin": round(gross_margin, 4), "Profit Margin": round(profit_margin, 4), "ROA": round(roa, 4), "ROE": round(roe, 4)},
        "DuPont_Breakdown": {
            "Profitability_Lever": round(profit_margin, 4),
            "Efficiency_Lever": round(total_asset_turnover, 2),
            "Leverage_Lever": round(equity_multiplier, 2),
            "Calculated_ROE": round(dupont_roe, 4)
        },
        "Market": {"P/E": round(pe_ratio, 2), "Market/Book": round(market_to_book, 2), "Price/Sales": round(price_sales, 4), "EV": round(enterprise_value, 2), "EV_EBITDA": round(ev_ebitda, 2)},
        "Operational": {"Inv_Turnover": round(inv_turnover, 2), "DSI": round(days_sales_inv, 2), "Rec_Turnover": round(rec_turnover, 2), "DSO": round(days_sales_rec, 2)}
    }

    ai_report = construct_prompt_financial(financial_results)
    return financial_results, ai_report


def analyze_marketing_performance(
    Revenue, marketing_spend, new_customers_acquired,
    total_customers_start_period, total_customers_end_period,
    avg_revenue_per_user_monthly, gross_margin_pct, expansion_revenue
) -> tuple[dict, str]:
    """
    Compute marketing unit economics and generate CMO AI report.
    Returns (metrics_dict, ai_report_text).
    """
    cac = marketing_spend / new_customers_acquired if new_customers_acquired > 0 else 0

    lost_customers = (total_customers_start_period + new_customers_acquired) - total_customers_end_period
    churn_rate = lost_customers / total_customers_start_period if total_customers_start_period > 0 else 0
    retention_rate = 1 - churn_rate

    starting_rev = total_customers_start_period * avg_revenue_per_user_monthly
    nrr = (starting_rev + expansion_revenue - (lost_customers * avg_revenue_per_user_monthly)) / starting_rev if starting_rev > 0 else 0

    ltv = (avg_revenue_per_user_monthly * gross_margin_pct) / churn_rate if churn_rate > 0 else 0

    ltv_cac_ratio = ltv / cac if cac > 0 else 0
    payback_period = cac / (avg_revenue_per_user_monthly * gross_margin_pct) if avg_revenue_per_user_monthly > 0 and gross_margin_pct > 0 else 0

    marketing_efficiency_ratio = Revenue / marketing_spend if marketing_spend > 0 else 0
    marketing_spend_pct = marketing_spend / Revenue if Revenue > 0 else 0

    marketing_results = {
        "Acquisition": {
            "CAC": round(cac, 2),
            "Marketing_Spend_Pct": f"{marketing_spend_pct:.1%}",
            "Marketing_Efficiency_Ratio": round(marketing_efficiency_ratio, 2)
        },
        "Retention_and_Value": {
            "Retention_Rate": f"{retention_rate:.1%}",
            "Churn_Rate": f"{churn_rate:.1%}",
            "Net_Revenue_Retention": f"{nrr:.1%}",
            "LTV": round(ltv, 2)
        },
        "Unit_Economics": {
            "LTV_CAC_Ratio": round(ltv_cac_ratio, 2),
            "Payback_Period_Months": round(payback_period, 1),
            "Status": "Healthy" if ltv_cac_ratio >= 3 else "Needs Optimization"
        }
    }

    ai_report = construct_prompt_marketing(marketing_results)
    return marketing_results, ai_report


def analyze_business(
    Revenue, marketing_spend, new_customers_acquired,
    total_customers_start_period, total_customers_end_period,
    avg_revenue_per_user_monthly, gross_margin_pct, expansion_revenue,
    COGS, Gross_Profit, Sales_and_Marketing, Research_and_Development,
    General_and_Administrative, EBITDA, Depreciation_and_Amortization, EBIT,
    Interest_Expense, Net_Income, cash_equivalents, accounts_receivable,
    inventory, fixed_assets_ppe, intangible_assets, accounts_payable,
    accrued_expenses, long_term_debt, shareholders_equity,
    stock_price=0, shares_outstanding=1
) -> dict:
    """
    Run full business analysis: financial + marketing + CEO synthesis.
    Returns dict with financial_metrics, financial_report, marketing_metrics, marketing_report, ceo_report.
    """
    financial_metrics, financial_report = financial_analysis(
        Revenue, COGS, Gross_Profit, Sales_and_Marketing, Research_and_Development,
        General_and_Administrative, EBITDA, Depreciation_and_Amortization, EBIT,
        Interest_Expense, Net_Income, cash_equivalents, accounts_receivable,
        inventory, fixed_assets_ppe, intangible_assets, accounts_payable,
        accrued_expenses, long_term_debt, shareholders_equity,
        stock_price, shares_outstanding
    )

    marketing_metrics, marketing_report = analyze_marketing_performance(
        Revenue, marketing_spend, new_customers_acquired,
        total_customers_start_period, total_customers_end_period,
        avg_revenue_per_user_monthly, gross_margin_pct, expansion_revenue
    )

    ceo_report = construct_prompt_ceo(financial_report, marketing_report)

    return {
        "financial_metrics": financial_metrics,
        "financial_report": financial_report,
        "marketing_metrics": marketing_metrics,
        "marketing_report": marketing_report,
        "ceo_report": ceo_report,
    }
