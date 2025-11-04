import logging
import os
from pathlib import Path
from typing import List  # NOQA: UP035

from openai import OpenAI
import streamlit as st


def _read_api_key_from_local_secrets() -> str | None:
    """Try to read api_credentials.api_key from local .streamlit/secrets.toml.

    This is a minimal parser targeting the expected structure:
        [api_credentials]
        api_key = "sk-..."
    """
    candidates: list[Path] = []
    cwd = Path.cwd()
    candidates.append(cwd / ".streamlit" / "secrets.toml")

    here = Path(__file__).resolve()
    # Walk up a few parents to find a nearby .streamlit/secrets.toml
    for parent in list(here.parents)[:6]:
        candidates.append(parent / ".streamlit" / "secrets.toml")

    for secrets_path in candidates:
        if not secrets_path.is_file():
            continue
        try:
            current_section = None
            with secrets_path.open("r", encoding="utf-8") as fh:
                for raw_line in fh:
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("[") and line.endswith("]"):
                        current_section = line.strip("[]").strip()
                        continue
                    if current_section == "api_credentials" and line.startswith("api_key"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            value = parts[1].strip().strip('"').strip("'")
                            if value:
                                return value
        except Exception:
            # Try next candidate
            continue
    return None


def _get_openai_api_key() -> str:
    # 1) Prefer Streamlit Cloud/local app secrets
    try:
        # st.secrets behaves like a mapping; handle missing keys gracefully
        api_key = (
            st.secrets["api_credentials"]["api_key"]  # type: ignore[index]
            if "api_credentials" in st.secrets and "api_key" in st.secrets["api_credentials"]
            else None
        )
        if api_key:
            return str(api_key)
    except Exception:
        pass

    # 2) Environment variable (optional extra convenience)
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key

    # 3) Local .streamlit/secrets.toml
    file_key = _read_api_key_from_local_secrets()
    if file_key:
        return file_key

    raise RuntimeError(
        "OpenAI API key not found. Add it to Streamlit Cloud secrets or to a local .streamlit/secrets.toml (under [api_credentials].api_key), or set OPENAI_API_KEY."
    )


client = OpenAI(api_key=_get_openai_api_key())


@st.cache_data()
def loading_data(ai_model: str, messages: List[dict]) -> dict:
    logging.info(f"{messages=}")
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=ai_model,
    )
    logging.info(f"{chat_completion=}")
    return chat_completion

