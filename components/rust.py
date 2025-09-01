import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# ==============================
# Load .env (cari di root atau di components/utils)
# ==============================
def _load_env():
    root_env = Path(".") / ".env"
    utils_env = Path(__file__).parent / "utils" / ".env"

    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    elif utils_env.exists():
        load_dotenv(dotenv_path=utils_env)
    else:
        st.warning("⚠️ File .env tidak ditemukan di root maupun components/utils/")

_load_env()

# ==============================
# Inisialisasi Groq Client
# ==============================
@st.cache_resource
def _init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ Error 404: API Key tidak ditemukan.")
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Gagal inisialisasi Groq client: {e}")
        return None

groq_client = _init_groq_client()

# ==============================
# Fungsi Normalisasi Label
# ==============================
def _normalize_label(text):
    """Normalisasi label ke: Positif / Negatif / Netral"""
    if not isinstance(text, str):
        return "Netral"
    t = text.strip().lower()
    if "positif" in t or "positive" in t:
        return "Positif"
    if "negatif" in t or "negative" in t:
        return "Negatif"
    if "netral" in t or "neutral" in t:
        return "Netral"
    # fallback: coba cari kata kunci singkat
    if "pos" in t: return "Positif"
    if "neg" in t: return "Negatif"
    if "neu" in t: return "Netral"
    return "Netral"

# ==============================
# Fungsi Evaluasi Sentimen
# ==============================
def evaluate(text, sentiment_lokal):
    """
    Evaluasi ulang sentimen menggunakan Groq LLaMA.
    Jika gagal / tidak ada API key, kembalikan hasil lokal.
    """
    if groq_client is None:
        return sentiment_lokal
    try:
        prompt = (
            "Kamu adalah evaluator sentimen untuk tweet berbahasa Indonesia.\n"
            "Tugasmu menentukan label akhir: Positif, Negatif, atau Netral.\n"
            "Pertimbangkan juga prediksi model lokal sebagai referensi.\n\n"
            f"Tweet: \"{text}\"\n"
            f"Prediksi model lokal: {sentiment_lokal}\n\n"
            "Jawab hanya dengan salah satu kata ini: Positif, Negatif, atau Netral."
        )
        resp = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=8
        )
        raw = resp.choices[0].message.content.strip()
        return _normalize_label(raw)
    except Exception as e:
        st.warning(f"⚠️ Error Evaluasi Groq: {e}")
        return sentiment_lokal
