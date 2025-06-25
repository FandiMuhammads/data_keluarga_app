import streamlit as st
import os
st.write("Files in pages/:", os.listdir("pages"))

st.set_page_config(
    page_title="Dashboard Data Keluarga",
    page_icon="🏠",
    layout="centered"
)

st.title("🏡 Dashboard Pendataan Keluarga")

st.markdown("""
Selamat datang di aplikasi **Pendataan Keluarga** tahun 2024.

Silakan pilih halaman dari menu di sebelah kiri:
- 🧾 Input Data Kepala Keluarga (form_keluarga)
- 🧑‍🤝‍🧑 Input Data Anggota Keluarga (form_anggota)
""")
