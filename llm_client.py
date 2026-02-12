"""
LLM client for AI Business Consultant.
Supports Gemini, OpenAI, Ollama, and DeepSeek.
API keys are read from environment variables for security.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# LLM CONFIGURATION
# ===========================
MODEL_CONFIG = {
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4o",
    "ollama": "mistral",
    "deepseek": "deepseek-chat"
}

_llm_client = None


def _init_llm():
    """Initialize the LLM client based on provider."""
    global _llm_client
    llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if llm_provider == "gemini":
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY or GEMINI_API_KEY must be set in environment. "
                "Create a .env file with your API key."
            )
        genai.configure(api_key=api_key)
        _llm_client = genai.GenerativeModel(MODEL_CONFIG["gemini"])

    elif llm_provider == "openai":
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment.")
        _llm_client = OpenAI(api_key=api_key)

    elif llm_provider == "ollama":
        try:
            import ollama
        except ImportError:
            raise ImportError("Install ollama: pip install ollama")
        _llm_client = ollama

    elif llm_provider == "deepseek":
        from openai import OpenAI
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY must be set in environment.")
        _llm_client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")


def call_llm(prompt: str) -> str:
    """
    Unified function to call any LLM based on llm_provider.
    """
    global _llm_client
    llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    # Re-init if provider changed (e.g. user switched in UI)
    if _llm_client is None:
        _init_llm()

    if llm_provider == "gemini":
        response = _llm_client.generate_content(prompt)
        return response.text

    elif llm_provider == "openai":
        response = _llm_client.chat.completions.create(
            model=MODEL_CONFIG["openai"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    elif llm_provider == "ollama":
        response = _llm_client.generate(
            model=MODEL_CONFIG["ollama"],
            prompt=prompt,
            stream=False
        )
        return response["response"]

    elif llm_provider == "deepseek":
        response = _llm_client.chat.completions.create(
            model=MODEL_CONFIG["deepseek"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")
