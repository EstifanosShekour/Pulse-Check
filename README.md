# Pulse-Check

**AI Business Consultant** suited for small and medium-sized companies.

A web application that turns your financial and marketing data into strategic insights using AI. Get CFO, CMO, and CEO-level analysis in minutes.

## Features

- **CFO Financial Analysis**: Liquidity, solvency, profitability, DuPont analysis, and operational metrics
- **CMO Marketing Analysis**: LTV/CAC, churn, retention, payback period, unit economics
- **CEO Synthesis**: Strategic directives combining financial and marketing insights
- **Multiple LLM Support**: Gemini, OpenAI, Ollama, DeepSeek

## Quick Start

### 1. Install dependencies

```bash
git clone https://github.com/EstifanosShekour/Pulse-Check.git
cd Pulse-Check
pip install -r requirements.txt
```

### 2. Configure your API key

**Option A: Environment variable**
```bash
# Create a .env file (copy from .env.example)
# Add your Google API key (free at https://aistudio.google.com/apikey)
GOOGLE_API_KEY=your_key_here
LLM_PROVIDER=gemini
```

**Option B: Enter in the app**
- The web app has a sidebar where you can paste your API key at runtime
- Keys are only stored in your browser session

### 3. Run the web app

```bash
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter your data** (or use the sample data for a demo)
   - **Financial**: Income statement, balance sheet, optional market data
   - **Marketing**: Customer acquisition, retention, ARPU, expansion revenue

2. **Choose analysis type**
   - Full Analysis: CFO + CMO + CEO synthesis
   - Financial Only: CFO report
   - Marketing Only: CMO report

3. **Run Analysis** and review your AI-generated strategic reports

## LLM Providers

| Provider | Setup |
|----------|-------|
| **Gemini** | Free API key from [Google AI Studio](https://aistudio.google.com/apikey) |
| **OpenAI** | Paid API key from [OpenAI](https://platform.openai.com/api-keys) |
| **Ollama** | Local models - run `ollama pull mistral` |
| **DeepSeek** | API key from [DeepSeek](https://platform.deepseek.com) |

## Project Structure

```
Pulse-Check/
├── app.py              # Streamlit web application
├── analysis.py         # Business logic & AI prompts
├── llm_client.py       # LLM initialization & API calls
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API keys
└── README.md           # This file
```

## Security

- **Never commit API keys** to version control
- Use `.env` for local development (add `.env` to `.gitignore`)
- The app supports entering keys in the UI; they are not stored on disk
