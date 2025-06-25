import streamlit as st
import os


st.set_page_config(
    page_title="Dashboard Data Keluarga",
    page_icon="🏠",
    layout="centered"
)

st.title("🏡 Dashboard Pendataan Keluarga")

st.markdown("""
Selamat datang di aplikasi **Pendataan Keluarga**.

Silakan pilih halaman dari menu di sebelah kiri:
- 🧾 Input Data Kepala Keluarga (form_keluarga)
- 🧑‍🤝‍🧑 Input Data Anggota Keluarga (form_anggota)
""")
