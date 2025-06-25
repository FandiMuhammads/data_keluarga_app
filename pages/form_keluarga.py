import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

st.set_page_config(page_title="Form Kepala Keluarga", page_icon="🧾")

# --- Koneksi ke Google Sheets ---
@st.cache_resource
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gspread"]), scope)
    client = gspread.authorize(creds)
    return client

client = connect_sheets()
sheet_keluarga = client.open("Data_Keluarga_DesaCantik").worksheet("keluarga")

# --- Form Input ---
st.title("🧾 Form Pendataan Kepala Keluarga")

with st.form("form_keluarga"):
    st.subheader("Wilayah")
    provinsi = st.text_input("Provinsi", st.session_state.get("provinsi", "Sumatera Utara"))
    kabupaten = st.text_input("Kabupaten", st.session_state.get("kabupaten", "Labuhanbatu Utara"))
    kecamatan = st.text_input("Kecamatan", st.session_state.get("kecamatan", ""))
    desa = st.text_input("Desa", st.session_state.get("desa", "SIDUA-DUA"))
    dusun = st.text_input("Dusun", st.session_state.get("dusun", ""))
    alamat = st.text_area("Alamat", st.session_state.get("alamat", ""))

    st.subheader("Keterangan Petugas")
    pendata = st.text_input("Nama Petugas Pendataan", st.session_state.get("pendata", ""))
    pengawas = st.text_input("Nama Petugas Pengawas", st.session_state.get("pengawas", ""))
    tanggal = st.date_input("Tanggal", st.session_state.get("tanggal", datetime.date.today()))

    st.subheader("Data Keluarga")
    no_kk = st.text_input("Nomor Kartu Keluarga", st.session_state.get("no_kk", ""))
    kepala_keluarga = st.text_input("Nama Kepala Keluarga", st.session_state.get("kepala_keluarga", ""))
    jumlah_anggota = st.number_input("Jumlah Anggota Keluarga", min_value=1, max_value=20, step=1, value=st.session_state.get("jumlah", 1))

    submitted = st.form_submit_button("Simpan & Lanjut")

# --- Logika Simpan ---
if submitted:
    st.session_state.update({
        "provinsi": provinsi,
        "kabupaten": kabupaten,
        "kecamatan": kecamatan,
        "desa": desa,
        "dusun": dusun,
        "alamat": alamat,
        "pendata": pendata,
        "pengawas": pengawas,
        "tanggal": tanggal,
        "no_kk": no_kk,
        "kepala_keluarga": kepala_keluarga,
        "jumlah": int(jumlah_anggota),
        "current_index": 1
    })

    # Validasi isian wajib
    required_fields = [provinsi, kabupaten, kecamatan, desa, dusun, alamat,
                       pendata, pengawas, no_kk, kepala_keluarga]
    if any(not field.strip() for field in required_fields):
        st.warning("❗ Semua kolom harus diisi sebelum melanjutkan.")
        st.stop()

    # Validasi panjang No KK
    if len(no_kk) != 16 or not no_kk.isdigit():
        st.warning("❗ Nomor KK harus terdiri dari 16 digit angka.")
        st.stop()

    no_kk_list = sheet_keluarga.col_values(10)
    if no_kk in no_kk_list:
        st.warning("❗ Nomor KK ini sudah pernah diinput.")
        st.stop()

    data = [provinsi, kabupaten, kecamatan, desa, dusun, alamat,
            pendata, pengawas, str(tanggal), no_kk, kepala_keluarga, int(jumlah_anggota)]
    sheet_keluarga.append_row(data)

    st.success("✅ Data kepala keluarga disimpan.")
    st.switch_page("form_anggota.py")
