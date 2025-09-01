# import streamlit as st
# import os
# import subprocess
# import glob

# def render():
#     st.subheader("📥 Ambil Data dari Twitter")

#     if st.session_state.selected_keyword:
#         st.markdown(f"**Kata Kunci:** `{st.session_state.selected_keyword}`")
#     else:
#         st.warning("⚠️ Belum ada kata kunci yang dipilih.")

#     limit = st.number_input("📌 Jumlah tweet", 10, 1000, 100, 10)

#     output_folder = "tweets-data"
#     os.makedirs(output_folder, exist_ok=True)
#     twitter_auth_token = "7c61b36f86f134a53c742564e0f592960648b33c"

#     if st.button("📥 Ambil Data"):
#         if not st.session_state.selected_keyword:
#             st.warning("⚠️ Pilih kata kunci dulu di tab Beranda.")
#         else:
#             command = f"npx tweet-harvest -o {output_folder} -s \"{st.session_state.selected_keyword}\" --tab LATEST -l {limit} --token {twitter_auth_token}"
#             with st.spinner("📥 Mengambil data..."):
#                 result = subprocess.run(command, shell=True, text=True, capture_output=True)
#             if result.returncode == 0:
#                 csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
#                 if csv_files:
#                     st.session_state.filename = max(csv_files, key=os.path.getctime)
#                     st.success("✅ Data berhasil diambil.")
#                 else:
#                     st.error("❌ CSV tidak ditemukan.")
#             else:
#                 st.error(f"❌ Error: {result.stderr}")
