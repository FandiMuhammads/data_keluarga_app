import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

st.set_page_config(page_title="Form Anggota Keluarga", page_icon="🧑‍🤝‍🧑")

@st.cache_resource
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    return gspread.authorize(creds)

client = connect_sheets()
sheet_anggota = client.open("Data_Keluarga_DesaCantik").worksheet("anggota_keluarga")

# Validasi
if 'jumlah' not in st.session_state or 'no_kk' not in st.session_state:
    st.warning("Silakan isi form kepala keluarga terlebih dahulu.")
    st.stop()

# Inisialisasi indeks
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 1

idx = st.session_state['current_index']
jumlah = st.session_state['jumlah']
no_kk = st.session_state['no_kk']

st.title(f"🧑‍🤝‍🧑 Form Anggota Keluarga ke-{idx} dari {jumlah}")
st.caption(f"Nomor KK: {no_kk}")

# --- Form Anggota ---
with st.form("form_anggota"):
    nama = st.text_input("Nama Anggota")
    nik = st.text_input("NIK")
    keberadaan = st.selectbox("Keberadaan", ["Domisili sesuai KK", "Tidak sesuai KK", "Meninggal"])
    jenis_kelamin = st.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    tgl_lahir = st.date_input("Tanggal Lahir")
    umur = st.number_input("Umur", min_value=0)
    pendidikan = st.selectbox("Ijazah Tertinggi", ["Tidak tamat SD", "SD/Sederajat", "SMP", "SMA", "Perguruan Tinggi"])
    status_nikah = st.selectbox("Status Perkawinan", ["Belum Kawin", "Cerai Hidup", "Kawin", "Cerai Mati"])
    hub_keluarga = st.selectbox("Hubungan", ["Kepala Rumah Tangga", "Suami/Istri", "Anak", "Cucu", "Orangtua/Mertua", "Famili Lain"])
    status_pekerjaan = st.selectbox("Status Pekerjaan", ["Tidak Bekerja", "Berusaha Sendiri", "Buruh/Karyawan", "Pegawai"])
    pekerjaan = st.text_input("Pekerjaan Utama")
    bidang_usaha = st.selectbox("Lapangan Usaha", [
        "Pertanian", "Industri", "Konstruksi", "Perdagangan",
        "Penyediaan makan/minum", "Administrasi", "Pemerintahan",
        "Pendidikan", "Kesehatan", "Lainnya"
    ])
    submitted = st.form_submit_button("Simpan & Lanjut")

if submitted:
    # Validasi panjang NIK
    if len(nik) != 16 or not nik.isdigit():
        st.warning("❗ NIK harus terdiri dari 16 digit angka.")
        st.stop()

    # Validasi semua kolom terisi
    required_fields = [nama, nik, keberadaan, jenis_kelamin, pendidikan,
                       status_nikah, hub_keluarga, status_pekerjaan, pekerjaan, bidang_usaha]
    if any(not str(field).strip() for field in required_fields):
        st.warning("❗ Semua kolom wajib diisi.")
        st.stop()

    # Validasi duplikasi NIK
    nik_list = sheet_anggota.col_values(4)
    if nik in nik_list:
        st.warning("❗ NIK ini sudah pernah diinput.")
        st.stop()

    row = [
        no_kk, idx, nama, nik, keberadaan, jenis_kelamin, str(tgl_lahir),
        umur, pendidikan, status_nikah, hub_keluarga, status_pekerjaan,
        pekerjaan, bidang_usaha
    ]
    sheet_anggota.append_row(row)
    st.success(f"✅ Data anggota ke-{idx} disimpan.")

    if idx < jumlah:
        st.session_state['current_index'] += 1
        st.rerun()
    else:
        st.success("🎉 Semua anggota telah diinput.")
        st.balloons()
