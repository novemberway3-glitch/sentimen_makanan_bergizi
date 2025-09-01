# import streamlit as st

# def render(allowed_keywords):
#     st.markdown("""
#     <div style="padding:20px; background:white; border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
#         <h2>Selamat Datang di Aplikasi Twitter Sentiment Analysis 📊</h2>
#         <p>Aplikasi ini dirancang untuk mengumpulkan data dari Twitter berdasarkan kata kunci tertentu, 
#         kemudian melakukan <b>analisis sentimen</b> terhadap tweet tersebut. Hasil analisis akan divisualisasikan
#         dalam bentuk <b>diagram pie</b> dan <b>WordCloud</b>.</p>
#         <h3>🔍 Fitur Utama:</h3>
#         <ul>
#             <li>Ambil data tweet berdasarkan kata kunci.</li>
#             <li>Preprocessing teks.</li>
#             <li>Analisis sentimen menggunakan model berbasis AI.</li>
#             <li>Visualisasi sentimen dan WordCloud.</li>
#             <li>Download hasil analisis dalam format CSV.</li>
#         </ul>
#         <h3>📘 Panduan Penggunaan:</h3>
#         <ol>
#             <li>Pilih salah satu kata kunci di bawah.</li>
#             <li>Aplikasi otomatis pindah ke tab <b>Ambil Data</b> dan siap mengunduh tweet.</li>
#         </ol>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<h3 style='margin-top:20px;'>🎯 Pilih Kata Kunci Cepat:</h3>", unsafe_allow_html=True)

#     if "selected_keyword" in st.session_state and st.session_state.selected_keyword:
#         st.markdown(f"""
#         <div style="padding:10px; background:#e8f4ff; border-radius:8px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; border:1px solid #b3d8ff;">
#             <span style="font-size:16px; color:#333;">✅ Kata kunci terpilih: <b>{st.session_state.selected_keyword}</b></span>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("❌ Ganti Kata Kunci"):
#             st.session_state.selected_keyword = None
#             st.session_state.switch_to_tab = 0
#             st.rerun()

#     if not st.session_state.get("selected_keyword"):
#         st.markdown('<div class="beranda-keyword-row" style="display:flex; gap:10px;">', unsafe_allow_html=True)
#         cols = st.columns(len(allowed_keywords))
#         for idx, kw in enumerate(allowed_keywords):
#             with cols[idx]:
#                 if st.button(kw, key=f"kw_{idx}", use_container_width=True):
#                     st.session_state.selected_keyword = kw
#                     st.session_state.switch_to_tab = 1
#                     st.rerun()
#         st.markdown('</div>', unsafe_allow_html=True)
