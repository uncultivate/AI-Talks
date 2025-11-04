import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def loading_data(ai_model: str, messages: List[dict], *, max_completion_tokens: int = 2056, temperature: float = 1.0) -> dict:
    """Load chat completion data from OpenAI API. Not cached to ensure fresh responses.
    
    Note: GPT-5 models use reasoning tokens, so we need more tokens to allow for both
    reasoning and actual output. 512 tokens should be sufficient for short responses.
    """
    start = time.perf_counter()
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=ai_model,
        max_completion_tokens=max_completion_tokens,
        temperature=temperature,
    )
    duration = time.perf_counter() - start
    logging.info("openai.chat.completions.create duration: %.2fs", duration)
    return chat_completion


def loading_data_many(ai_model: str, bm_to_messages: dict, *, max_completion_tokens: int = 2056, temperature: float = 1.0) -> dict:
    """Execute multiple chat completion requests concurrently.

    bm_to_messages maps a key (e.g. 'bm1') to its messages list.
    Returns a mapping of the same keys to the completion objects.
    """
    results: dict = {}
    start_all = time.perf_counter()

    def _call(messages: List[dict]):
        return client.chat.completions.create(
            messages=messages,
            model=ai_model,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
        )

    with ThreadPoolExecutor(max_workers=min(8, max(1, len(bm_to_messages)))) as executor:
        future_to_key = {executor.submit(_call, msgs): key for key, msgs in bm_to_messages.items()}
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as exc:  # noqa: BLE001
                logging.exception("OpenAI call failed for %s: %s", key, exc)
                results[key] = None

    logging.info("parallel completions duration: %.2fs", time.perf_counter() - start_all)
    return results

