import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari folder
all_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/dashboard/main_data.csv")


