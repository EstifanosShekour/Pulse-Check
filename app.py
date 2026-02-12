"""
AI Business Consultant - Streamlit Web Application
Turn your financial and marketing data into strategic insights.
"""

import os
import streamlit as st
from analysis import financial_analysis, analyze_marketing_performance, analyze_business

# Page config
st.set_page_config(
    page_title="AI Business Consultant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .report-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f2f6 0%, #e8eaed 100%);
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "api_configured" not in st.session_state:
        st.session_state.api_configured = False
    if "results" not in st.session_state:
        st.session_state.results = None


def configure_llm():
    """Configure LLM in sidebar."""
    st.sidebar.header("🔑 API Configuration")
    st.sidebar.caption("Configure your LLM provider. Keys are stored in session only.")

    provider = st.sidebar.selectbox(
        "LLM Provider",
        ["gemini", "openai", "ollama", "deepseek"],
        index=0,
        help="Gemini is free with Google AI Studio. Ollama runs locally."
    )

    api_key = None
    if provider in ["gemini"]:
        api_key = st.sidebar.text_input(
            "Google API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Get a free key at https://aistudio.google.com/apikey"
        )
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            os.environ["LLM_PROVIDER"] = provider
    elif provider in ["openai"]:
        api_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Get a key at https://platform.openai.com/api-keys"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["LLM_PROVIDER"] = provider
    elif provider in ["deepseek"]:
        api_key = st.sidebar.text_input(
            "DeepSeek API Key",
            type="password",
            placeholder="sk-...",
            help="Get a key at https://platform.deepseek.com"
        )
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            os.environ["LLM_PROVIDER"] = provider
    else:
        os.environ["LLM_PROVIDER"] = provider
        st.sidebar.info("Ensure Ollama is running locally (ollama pull mistral)")

    return api_key or provider == "ollama"


def get_financial_form():
    """Render financial data form and return values."""
    st.subheader("📈 Financial Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Income Statement**")
        revenue = st.number_input("Revenue ($)", min_value=0, value=1_200_000, step=10_000)
        cogs = st.number_input("Cost of Goods Sold ($)", min_value=0, value=420_000, step=10_000)
        gross_profit = st.number_input("Gross Profit ($)", min_value=0, value=780_000, step=10_000)
        sales_marketing = st.number_input("Sales & Marketing ($)", min_value=0, value=200_000, step=5_000)
        rd = st.number_input("R&D ($)", min_value=0, value=120_000, step=5_000)
        gna = st.number_input("General & Admin ($)", min_value=0, value=150_000, step=5_000)
        ebitda = st.number_input("EBITDA ($)", min_value=0, value=310_000, step=10_000)
        dep_amort = st.number_input("Depreciation & Amortization ($)", min_value=0, value=40_000, step=1_000)
        ebit = st.number_input("EBIT ($)", min_value=0, value=270_000, step=10_000)
        interest = st.number_input("Interest Expense ($)", min_value=0, value=12_000, step=1_000)
        net_income = st.number_input("Net Income ($)", value=203_820, step=1_000)

    with col2:
        st.markdown("**Balance Sheet**")
        cash = st.number_input("Cash & Equivalents ($)", min_value=0, value=250_000, step=10_000)
        ar = st.number_input("Accounts Receivable ($)", min_value=0, value=95_000, step=5_000)
        inv = st.number_input("Inventory ($)", min_value=0, value=180_000, step=5_000)
        ppe = st.number_input("Fixed Assets (PP&E) ($)", min_value=0, value=400_000, step=10_000)
        intangibles = st.number_input("Intangible Assets ($)", min_value=0, value=100_000, step=5_000)
        ap = st.number_input("Accounts Payable ($)", min_value=0, value=60_000, step=5_000)
        accrued = st.number_input("Accrued Expenses ($)", min_value=0, value=25_000, step=5_000)
        ltd = st.number_input("Long-term Debt ($)", min_value=0, value=350_000, step=10_000)
        equity = st.number_input("Shareholders' Equity ($)", min_value=0, value=600_000, step=10_000)

    with col3:
        st.markdown("**Market Data (Optional)**")
        stock_price = st.number_input("Stock Price ($)", min_value=0.0, value=45.0, step=0.5)
        shares = st.number_input("Shares Outstanding", min_value=1, value=50_000, step=1_000)

    return {
        "Revenue": revenue, "COGS": cogs, "Gross_Profit": gross_profit,
        "Sales_and_Marketing": sales_marketing, "Research_and_Development": rd,
        "General_and_Administrative": gna, "EBITDA": ebitda,
        "Depreciation_and_Amortization": dep_amort, "EBIT": ebit,
        "Interest_Expense": interest, "Net_Income": net_income,
        "cash_equivalents": cash, "accounts_receivable": ar, "inventory": inv,
        "fixed_assets_ppe": ppe, "intangible_assets": intangibles,
        "accounts_payable": ap, "accrued_expenses": accrued,
        "long_term_debt": ltd, "shareholders_equity": equity,
        "stock_price": stock_price, "shares_outstanding": shares
    }


def get_marketing_form():
    """Render marketing data form and return values."""
    st.subheader("📣 Marketing & Customer Data")

    col1, col2 = st.columns(2)

    with col1:
        marketing_spend = st.number_input("Marketing Spend ($)", min_value=0, value=75_000, step=5_000)
        new_customers = st.number_input("New Customers Acquired", min_value=0, value=300, step=10)
        customers_start = st.number_input("Customers at Start of Period", min_value=0, value=2_000, step=100)
        customers_end = st.number_input("Customers at End of Period", min_value=0, value=2_200, step=100)

    with col2:
        arpu = st.number_input("Avg Revenue Per User/Month ($)", min_value=0.0, value=150.0, step=5.0)
        gross_margin_pct = st.number_input("Gross Margin % (0-1)", min_value=0.0, max_value=1.0, value=0.65, step=0.01, format="%.2f")
        expansion_revenue = st.number_input("Expansion Revenue ($)", min_value=0, value=12_000, step=1_000)

    return {
        "marketing_spend": marketing_spend,
        "new_customers_acquired": new_customers,
        "total_customers_start_period": customers_start,
        "total_customers_end_period": customers_end,
        "avg_revenue_per_user_monthly": arpu,
        "gross_margin_pct": gross_margin_pct,
        "expansion_revenue": expansion_revenue
    }


def display_results(results: dict):
    """Display analysis results in expandable sections."""
    st.success("Analysis complete! Review your reports below.")

    tabs = st.tabs(["📊 CFO Report", "📣 CMO Report", "👔 CEO Synthesis", "📈 Raw Metrics"])

    with tabs[0]:
        st.markdown("### CFO Financial Analysis")
        st.markdown("---")
        st.markdown(results["financial_report"])

    with tabs[1]:
        st.markdown("### CMO Marketing Analysis")
        st.markdown("---")
        st.markdown(results["marketing_report"])

    with tabs[2]:
        st.markdown("### CEO Business Synthesis")
        st.markdown("---")
        st.markdown(results["ceo_report"])

    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            st.json(results["financial_metrics"])
        with col2:
            st.json(results["marketing_metrics"])


def main():
    init_session_state()

    st.markdown('<p class="main-header">📊 AI Business Consultant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your financial and marketing data into strategic insights powered by AI</p>', unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        if configure_llm():
            st.session_state.api_configured = True
        else:
            st.session_state.api_configured = False
            st.warning("Enter your API key to enable analysis.")

    # Load sample data button
    use_sample = st.checkbox("Use sample data for demo", value=True, help="Pre-fill with example business data")

    if use_sample:
        st.info("Using sample data. Uncheck to enter your own numbers.")
        # Forms will still render with default values from get_*_form

    # Data collection
    financial_data = get_financial_form()
    st.divider()
    marketing_data = get_marketing_form()

    # Merge for full analysis
    all_data = {**financial_data, **marketing_data}

    st.divider()

    # Analysis options
    analysis_type = st.radio(
        "Analysis Type",
        ["Full Analysis (Financial + Marketing + CEO)", "Financial Only", "Marketing Only"],
        horizontal=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

    if run_analysis:
        if not st.session_state.api_configured:
            st.error("Please configure your API key in the sidebar first.")
            return

        with st.spinner("Analyzing your business... This may take 30-60 seconds."):
            try:
                if analysis_type == "Full Analysis (Financial + Marketing + CEO)":
                    results = analyze_business(**all_data)
                    display_results(results)
                elif analysis_type == "Financial Only":
                    metrics, report = financial_analysis(**financial_data)
                    st.success("Analysis complete!")
                    st.markdown("### CFO Financial Analysis")
                    st.markdown("---")
                    st.markdown(report)
                    with st.expander("View Raw Metrics"):
                        st.json(metrics)
                else:
                    metrics, report = analyze_marketing_performance(
                        Revenue=financial_data["Revenue"],
                        **marketing_data
                    )
                    st.success("Analysis complete!")
                    st.markdown("### CMO Marketing Analysis")
                    st.markdown("---")
                    st.markdown(report)
                    with st.expander("View Raw Metrics"):
                        st.json(metrics)
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()
