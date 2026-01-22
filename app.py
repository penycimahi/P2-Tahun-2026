import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Dashboard P2 2026", layout="wide", page_icon="📊")

st.title("📊 Dashboard Monitoring P2 - Tahun 2026")
st.markdown("---")

# 2. FUNGSI AMBIL DATA (Ubah Link ke format Export CSV)
@st.cache_data(ttl=600) # Data disimpan selama 10 menit sebelum refresh otomatis
def fetch_data(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

# ID Spreadsheet kamu (diambil dari link yang kamu kasih)
ID_MUTU = "1VcP9HbzWdqMCQStG0644ter6xYF3gkgOVrO68qaYhYI"
ID_LVL2 = "1QFWOrmO1FNi6YP_Qc4jjtOUgcvzTwYY1i35bQ-13pRk"
ID_LVL1 = "1tGvFL5XJ_WWVG80Gt70z3kx56NmnftDBydC23Rmb7iA"

# Load Data
try:
    df_mutu = fetch_data(ID_MUTU)
    df_lvl2 = fetch_data(ID_LVL2)
    df_lvl1 = fetch_data(ID_LVL1)
    data_ready = True
except Exception as e:
    st.error(f"Waduh, ada masalah koneksi: {e}")
    data_ready = False

# 3. TAMPILAN DASHBOARD
if data_ready:
    # --- BAGIAN ATAS: RINGKASAN (METRICS) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data Mutu", f"{len(df_mutu)} Baris")
    col2.metric("Total Eval Level 2", f"{len(df_lvl2)} Baris")
    col3.metric("Total Eval Level 1", f"{len(df_lvl1)} Baris")
    
    st.markdown("---")

    # --- BAGIAN TENGAH: DETAIL DATA (TABS) ---
    tab1, tab2, tab3 = st.tabs(["🛡️ Penjaminan Mutu", "📈 Evaluasi Level 2", "📋 Evaluasi Level 1"])

    with tab1:
        st.subheader("Detail Data Penjaminan Mutu")
        st.dataframe(df_mutu, use_container_width=True)
        # Contoh Grafik sederhana (Ganti 'Nama Kolom' dengan nama kolom yang ada di sheet-mu)
        # st.bar_chart(df
