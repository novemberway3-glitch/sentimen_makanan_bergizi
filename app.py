import streamlit as st
import subprocess
import pandas as pd
import os
import re
import glob
import pickle
import torch
import tempfile
import gdown
from transformers import AutoTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from components.rust import evaluate

# ==============================
# Konfigurasi Halaman
# ==============================
load_dotenv()
st.set_page_config(page_title="Twitter Sentiment App", page_icon="📊", layout="wide")
st.title("📊 Twitter Sentiment Analysis")

# ==============================
# Session State
# ==============================
if "selected_keyword" not in st.session_state:
    st.session_state.selected_keyword = ""
if "filename" not in st.session_state:
    st.session_state.filename = None
if "switch_to_tab" not in st.session_state:
    st.session_state.switch_to_tab = None

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #d4fc79, #96e6a1);
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}
h1 { text-align: center; color: #1b4332; font-weight: 700; }
h2 { color: #2d6a4f; }
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f9f9f9);
    padding: 20px; border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}
button[kind="primary"] {
    background: linear-gradient(90deg, #43cea2, #185a9d) !important;
    border-radius: 12px !important;
    color: white !important; font-weight: bold !important; border: none !important;
}
button[kind="secondary"] {
    border-radius: 8px !important;
    background-color: #2d6a4f !important;
    color: white !important;
    font-weight: 600 !important; font-size: 14px !important;
    transition: all 0.2s ease;
}
button[kind="secondary"]:hover { background-color: #40916c !important; transform: scale(1.02); }

.beranda-keyword-row [data-testid="column"] { padding-left: 0 !important; padding-right: 5px !important; }
.beranda-keyword-row [data-testid="column"]:last-child { padding-right: 0 !important; }

[data-testid="stToolbar"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# JavaScript untuk auto-switch tab
# ==============================
st.markdown("""
<script>
function switchTab(tabIndex){
    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
    if (tabs && tabs.length > tabIndex){
        tabs[tabIndex].click();
    }
}
</script>
""", unsafe_allow_html=True)

# ==============================
# Tabs
# ==============================
tabs = st.tabs(["🏠 Beranda", "📥 Ambil Data", "📊 Analisis & Visualisasi"])

# Jika ada flag pindah tab
if st.session_state.switch_to_tab is not None:
    st.markdown(f"<script>switchTab({int(st.session_state.switch_to_tab)});</script>", unsafe_allow_html=True)
    st.session_state.switch_to_tab = None

# ==============================
# Tools & Stopwords
# ==============================
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_words = {
    'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'dengan',
    'pada', 'juga', 'karena', 'ada', 'tidak', 'sudah', 'saja', 'lebih',
    'akan', 'bagi', 'para', 'sebagai', 'oleh', 'tentang', 'maka', 'atau',
    'jadi', 'namun'
}

def clean_text(text):
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+|www\S+|pic.twitter\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    return text.lower().strip()

def remove_stopwords(text):
    return " ".join([w for w in text.split() if w not in stop_words])

def tokenize_text(text):
    return text.split()

allowed_keywords = [
    "kebijakan makanan siang gratis",
    "makan siang bergizi di sekolah",
    "program makanan bergizi"
]

def filter_by_keywords(text):
    return any(kw in text.lower() for kw in allowed_keywords)

# ==============================
# Load Model Lokal
# ==============================
@st.cache_resource
def load_local_model():
    try:
        file_id = "1wvY7Zi73zRgx24GH0_6NLOdB76gjnn5T"
        drive_url = f"https://drive.google.com/uc?id={file_id}"
        temp_path = os.path.join(tempfile.gettempdir(), "model_temp.pkl")

        if not os.path.exists(temp_path):
            with st.spinner("📥 Mengunduh model dari Google Drive..."):
                gdown.download(drive_url, temp_path, quiet=False)

        with open(temp_path, "rb") as f:
            model = pickle.load(f)

        if not hasattr(model.config, "output_attentions"):
            model.config.output_attentions = False
        if not hasattr(model.config, "output_hidden_states"):
            model.config.output_hidden_states = False

        tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
        return model, tokenizer
    except Exception as e:
        st.error(f"❌ Gagal memuat model lokal: {e}")
        return None, None

local_model, local_tokenizer = load_local_model()

def is_berita_comment(text):
    return bool(re.search(r"http\S+|www\S+|pic.twitter\S+", text) or "#" in text)

def predict_sentiment_local(texts):
    results = []
    if local_model and local_tokenizer:
        for txt in texts:
            if is_berita_comment(txt):
                results.append("Netral")
                continue
            inputs = local_tokenizer(txt, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = local_model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=1)
                label_map = {0: "Negatif", 1: "Positif", 2: "Netral"}
                results.append(label_map[predictions.item()])
    else:
        results = ["Netral"] * len(texts)
    return results

# ==============================
# Tab 1: Beranda
# ==============================
with tabs[0]:
    st.markdown("""
    <div style="padding:20px; background:white; border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
        <h2>Selamat Datang di Aplikasi Twitter Sentiment Analysis 📊</h2>
        <p>Aplikasi ini dirancang untuk mengumpulkan data dari Twitter berdasarkan kata kunci tertentu, 
        kemudian melakukan <b>analisis sentimen</b> terhadap tweet tersebut. Hasil analisis akan divisualisasikan
        dalam bentuk <b>diagram pie</b> dan <b>WordCloud</b>.</p>
        <h3>🔍 Fitur Utama:</h3>
        <ul>
            <li>Ambil data tweet berdasarkan kata kunci.</li>
            <li>Preprocessing teks.</li>
            <li>Analisis sentimen menggunakan model berbasis AI.</li>
            <li>Visualisasi sentimen dan WordCloud.</li>
            <li>Download hasil analisis dalam format CSV.</li>
        </ul>
        <h3>📘 Panduan Penggunaan:</h3>
        <ol>
            <li>Pilih salah satu kata kunci di bawah.</li>
            <li>Aplikasi otomatis pindah ke tab <b>Ambil Data</b> dan siap mengunduh tweet.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:20px;'>🎯 Pilih Kata Kunci Cepat:</h3>", unsafe_allow_html=True)

    # Jika keyword sudah dipilih, tampilkan notifikasi + tombol X
    if "selected_keyword" in st.session_state and st.session_state.selected_keyword:
        st.markdown(f"""
        <div style="padding:10px; background:#e8f4ff; border-radius:8px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; border:1px solid #b3d8ff;">
            <span style="font-size:16px; color:#333;">✅ Kata kunci terpilih: <b>{st.session_state.selected_keyword}</b></span>
        </div>
        """, unsafe_allow_html=True)

        # Tombol X untuk hapus
        if st.button("❌ Ganti Kata Kunci"):
            st.session_state.selected_keyword = None
            st.session_state.switch_to_tab = 0
            st.rerun()

    # Tampilkan pilihan keyword jika belum dipilih
    if not st.session_state.get("selected_keyword"):
        st.markdown('<div class="beranda-keyword-row" style="display:flex; gap:10px;">', unsafe_allow_html=True)
        cols = st.columns(len(allowed_keywords))
        for idx, kw in enumerate(allowed_keywords):
            with cols[idx]:
                if st.button(kw, key=f"kw_{idx}", use_container_width=True):
                    st.session_state.selected_keyword = kw
                    st.session_state.switch_to_tab = 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# Tab 2: Ambil Data
# ==============================
with tabs[1]:
    st.subheader("📥 Ambil Data dari Twitter")

    if st.session_state.selected_keyword:
        st.markdown(f"**Kata Kunci:** `{st.session_state.selected_keyword}`")
    else:
        st.warning("⚠️ Belum ada kata kunci yang dipilih.")

    limit = st.number_input("📌 Jumlah tweet", 10, 1000, 100, 10)

    output_folder = "tweets-data"
    os.makedirs(output_folder, exist_ok=True)
    twitter_auth_token = "7c61b36f86f134a53c742564e0f592960648b33c"

    if st.button("📥 Ambil Data"):
        if not st.session_state.selected_keyword:
            st.warning("⚠️ Pilih kata kunci dulu di tab Beranda.")
        else:
            command = f"npx tweet-harvest -o {output_folder} -s \"{st.session_state.selected_keyword}\" --tab LATEST -l {limit} --token {twitter_auth_token}"
            with st.spinner("📥 Mengambil data..."):
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
            if result.returncode == 0:
                csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
                if csv_files:
                    st.session_state.filename = max(csv_files, key=os.path.getctime)
                    st.success("✅ Data berhasil diambil.")
                else:
                    st.error("❌ CSV tidak ditemukan.")
            else:
                st.error(f"❌ Error: {result.stderr}")

# ==============================
# Tab 3: Analisis & Visualisasi
# ==============================
with tabs[2]:
    data_folder = "tweets-data"

    if not st.session_state.filename:
        csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
        if csv_files:
            st.session_state.filename = max(csv_files, key=os.path.getctime)

    if st.session_state.filename and os.path.exists(st.session_state.filename):
        df = pd.read_csv(st.session_state.filename)
        if df.empty:
            st.warning("⚠️ Tidak ada tweet yang cocok.")
        else:
            st.subheader("📋 Data Mentah")
            st.dataframe(df, use_container_width=True, height=400)

            text_columns = [c for c in df.columns if df[c].dtype == "object" and df[c].str.len().mean() > 10]
            if text_columns:
                selected_col = "full_text" if "full_text" in text_columns else text_columns[0]

                if st.button("📊 Analisis Data"):
                    with st.spinner("⏳ Analisis berjalan..."):
                        df["clean_text"] = df[selected_col].apply(clean_text)
                        df["no_stopwords"] = df["clean_text"].apply(remove_stopwords)
                        df["tokenized"] = df["no_stopwords"].apply(tokenize_text)
                        df["stemmed"] = df["tokenized"].apply(lambda t: " ".join(stemmer.stem(w) for w in t))

                        st.info("Mengevaluasi Sentimen...")

                        raw_texts = df[selected_col].tolist()
                        df["final_sentiment"] = [
                            evaluate(txt, predict_sentiment_local([txt])[0]) for txt in raw_texts
                        ]

                        st.subheader("📄 Hasil Preprocessing & Sentimen")
                        st.dataframe(df[[selected_col, "clean_text", "stemmed", "final_sentiment"]], use_container_width=True)

                        st.subheader("📊 Distribusi Sentimen")

                        sentiment_counts = df["final_sentiment"].value_counts().reset_index()
                        sentiment_counts.columns = ["Sentiment", "Count"]

                        # Pie Chart Donut dengan efek 3D
                        fig = px.pie(
                            sentiment_counts,
                            values="Count",
                            names="Sentiment",
                            hole=0.4,  # bikin jadi donut (efek 3D)
                        )

                        # Hilangkan background putih
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",  # background transparan
                            plot_bgcolor="rgba(0,0,0,0)",
                            showlegend=True,
                            title=dict(text="Distribusi Sentimen", font=dict(size=20))
                        )

                        # Efek "3D" dengan mempertebal border & shadow
                        fig.update_traces(
                            textposition="inside",
                            textinfo="percent+label",
                            marker=dict(line=dict(color="black", width=2))
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        st.subheader("☁️ WordCloud per Sentimen")
                        for label in df["final_sentiment"].unique():
                            text_data = " ".join(df[df["final_sentiment"] == label]["stemmed"])
                            if text_data.strip():
                                wc = WordCloud(width=800, height=400, background_color="white",
                                               max_words=100, colormap="Greens").generate(text_data)
                                fig_wc, ax = plt.subplots(figsize=(10, 5))
                                ax.imshow(wc, interpolation="bilinear")
                                ax.axis("off")
                                ax.set_title(f"WordCloud - {label}", fontsize=16, pad=20)
                                st.pyplot(fig_wc)

                        st.subheader("💾 Download Hasil Analisis")
                        output_csv = "hasil_analisis_sentimen.csv"
                        df.to_csv(output_csv, index=False)
            else:
                st.warning("⚠️ Tidak ada kolom teks yang valid.")
    else:
        st.info("ℹ️ Belum ada data di folder 'tweets-data'.")
