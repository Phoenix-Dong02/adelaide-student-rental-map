import streamlit as st
from deep_translator import GoogleTranslator


@st.cache_data(show_spinner=False)
def _translate_cached(text, target):
    # 只有成功的结果才会被缓存：一旦这里抛异常，st.cache_data 不会记录任何值
    return GoogleTranslator(source="auto", target=target).translate(text)


def translate_text(text, lang):
    """把用户输入的自由文本（标题、描述）翻译成当前语言；失败时返回原文"""
    if lang == "zh" or not isinstance(text, str) or not text.strip():
        return text
    try:
        return _translate_cached(text, lang) or text
    except Exception:
        return text
