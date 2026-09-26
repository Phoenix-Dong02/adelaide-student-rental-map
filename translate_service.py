import anthropic
import streamlit as st

TRANSLATE_SYSTEM_PROMPT = (
    "Translate the user's text into English. "
    "Output only the translation, with no explanation or preamble. "
    "Keep street names, suburb/area names, phone numbers and WeChat IDs exactly as written."
)


@st.cache_resource
def _get_client():
    # 不传 api_key，SDK 自动读取环境变量 ANTHROPIC_API_KEY
    return anthropic.Anthropic()


@st.cache_data(show_spinner=False)
def _translate_cached(text, target):
    # 只有成功的结果才会被缓存：一旦这里抛异常，st.cache_data 不会记录任何值
    response = _get_client().messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=TRANSLATE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    return "".join(block.text for block in response.content if block.type == "text").strip()


def translate_text(text, lang):
    """把用户输入的自由文本（标题、描述）翻译成当前语言；失败时返回原文"""
    if lang == "zh" or not isinstance(text, str) or not text.strip():
        return text
    try:
        return _translate_cached(text, lang) or text
    except Exception as e:
        print(f"[translate_text] {type(e).__name__}: {e}")
        return text
