# import streamlit as st
# import os
# import pandas as pd
# import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

# def render(clean_text, remove_stopwords, tokenize_text, stemmer,
#            predict_sentiment_local, evaluate_with_llama):
#     data_folder = "tweets-data"

#     if not st.session_state.filename:
#         csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
#         if csv_files:
#             st.session_state.filename = max(csv_files, key=os.path.getctime)

#     if st.session_state.filename and os.path.exists(st.session_state.filename):
#         df = pd.read_csv(st.session_state.filename)
#         if df.empty:
#             st.warning("⚠️ Tidak ada tweet yang cocok.")
#         else:
#             st.subheader("📋 Data Mentah")
#             st.dataframe(df, use_container_width=True, height=400)

#             text_columns = [c for c in df.columns if df[c].dtype == "object" and df[c].str.len().mean() > 10]
#             if text_columns:
#                 selected_col = "full_text" if "full_text" in text_columns else text_columns[0]

#                 if st.button("📊 Analisis Data"):
#                     with st.spinner("⏳ Analisis berjalan..."):
#                         df["clean_text"] = df[selected_col].apply(clean_text)
#                         df["no_stopwords"] = df["clean_text"].apply(remove_stopwords)
#                         df["tokenized"] = df["no_stopwords"].apply(tokenize_text)
#                         df["stemmed"] = df["tokenized"].apply(lambda t: " ".join(stemmer.stem(w) for w in t))

#                         st.info("Mengevaluasi Sentimen...")

#                         raw_texts = df[selected_col].tolist()
#                         df["final_sentiment"] = [
#                             evaluate_with_llama(txt, predict_sentiment_local([txt])[0]) for txt in raw_texts
#                         ]

#                         st.subheader("📄 Hasil Preprocessing & Sentimen")
#                         st.dataframe(df[[selected_col, "clean_text", "stemmed", "final_sentiment"]], use_container_width=True)

#                         st.subheader("📊 Distribusi Sentimen")
#                         sentiment_counts = df["final_sentiment"].value_counts().reset_index()
#                         sentiment_counts.columns = ["Sentiment", "Count"]

#                         fig = px.pie(
#                             sentiment_counts,
#                             values="Count",
#                             names="Sentiment",
#                             hole=0.4,
#                         )
#                         fig.update_layout(
#                             paper_bgcolor="rgba(0,0,0,0)",
#                             plot_bgcolor="rgba(0,0,0,0)",
#                             showlegend=True,
#                             title=dict(text="Distribusi Sentimen", font=dict(size=20))
#                         )
#                         fig.update_traces(
#                             textposition="inside",
#                             textinfo="percent+label",
#                             marker=dict(line=dict(color="black", width=2))
#                         )
#                         st.plotly_chart(fig, use_container_width=True)

#                         st.subheader("☁️ WordCloud per Sentimen")
#                         for label in df["final_sentiment"].unique():
#                             text_data = " ".join(df[df["final_sentiment"] == label]["stemmed"])
#                             if text_data.strip():
#                                 wc = WordCloud(width=800, height=400, background_color="white",
#                                                max_words=100, colormap="Greens").generate(text_data)
#                                 fig_wc, ax = plt.subplots(figsize=(10, 5))
#                                 ax.imshow(wc, interpolation="bilinear")
#                                 ax.axis("off")
#                                 ax.set_title(f"WordCloud - {label}", fontsize=16, pad=20)
#                                 st.pyplot(fig_wc)

#                         st.subheader("💾 Download Hasil Analisis")
#                         output_csv = "hasil_analisis_sentimen.csv"
#                         df.to_csv(output_csv, index=False)
#                         with open(output_csv, "rb") as f:
#                             st.download_button("⬇️ Download CSV", f, output_csv, "text/csv")
#             else:
#                 st.warning("⚠️ Tidak ada kolom teks yang valid.")
#     else:
#         st.info("ℹ️ Belum ada data di folder 'tweets-data'.")
