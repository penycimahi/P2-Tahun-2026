import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Evaluasi & Mutu", layout="wide")

st.title("📊 Dashboard Integrasi Data P2")
st.markdown("Data diambil secara realtime dari Google Sheets dan Excel 365")

# --- 1. KONFIGURASI LINK DATA ---
# Link Google Sheets (diubah ke format export CSV)
URL_MUTU = "https://docs.google.com/spreadsheets/d/1VcP9HbzWdqMCQStG0644ter6xYF3gkgOVrO68qaYhYI/export?format=csv"
URL_LVEL2 = "https://docs.google.com/spreadsheets/d/1QFWOrmO1FNi6YP_Qc4jjtOUgcvzTwYY1i35bQ-13pRk/export?format=csv"

# Link Excel 365 (Konversi dari embed ke download link)
URL_LEVEL1 = "https://kemenkeu-my.sharepoint.com/personal/fitroh_hastanto_kemenkeu_go_id/_layouts/15/download.aspx?sourcedoc={72337d60-0f83-4e2d-b437-c36a4470e7d6}"

# --- 2. FUNGSI LOAD DATA ---
@st.cache_data # Supaya aplikasi cepat dan tidak download terus-menerus
def load_data(url, file_type="csv"):
    try:
        if file_type == "csv":
            return pd.read_csv(url)
        else:
            return pd.read_excel(url)
    except Exception as e:
        return None

# Proses tarik data
df_mutu = load_data(URL_MUTU, "csv")
df_lvl2 = load_data(URL_LVEL2, "csv")
df_lvl1 = load_data(URL_LEVEL1, "excel")

# --- 3. TAMPILAN DASHBOARD ---
tab1, tab2, tab3, tab4 = st.tabs(["Penjaminan Mutu", "Evaluasi Level 2", "Evaluasi Level 1", "Gabungan (Ringkasan)"])

with tab1:
    st.header("Data Penjaminan Mutu")
    if df_mutu is not None:
        st.dataframe(df_mutu, use_container_width=True)
    else:
        st.error("Gagal memuat data Penjaminan Mutu. Pastikan akses sharing sudah 'Anyone with link'.")

with tab2:
    st.header("Data Evaluasi Level 2")
    if df_lvl2 is not None:
        st.dataframe(df_lvl2, use_container_width=True)
    else:
        st.error("Gagal memuat data Level 2.")

with tab3:
    st.header("Data Evaluasi Level 1 (Excel 365)")
    if df_lvl1 is not None:
        st.dataframe(df_lvl1, use_container_width=True)
    else:
        st.warning("Data Level 1 tidak bisa diakses. Pastikan link SharePoint diset 'Anyone with link' dan bukan privat.")

with tab4:
    st.header("Ringkasan Total Data")
    # Contoh visualisasi sederhana: Jumlah baris data di tiap file
    data_counts = {
        "Mutu": len(df_mutu) if df_mutu is not None else 0,
        "Level 2": len(df_lvl2) if df_lvl2 is not None else 0,
        "Level 1": len(df_lvl1) if df_lvl1 is not None else 0
    }
    st.bar_chart(pd.Series(data_counts))
    
    st.info("Tips: Kamu bisa menambahkan logika gabungan data (merge/concat) di sini sesuai kebutuhan kolom yang sama.")

# Tombol Refresh manual
if st.button('🔄 Update Data Sekarang'):
    st.cache_data.clear()
    st.rerun()
