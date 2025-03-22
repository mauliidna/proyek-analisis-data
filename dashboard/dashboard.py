import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset hasil cleaning
all_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/main/dashboard/main_data.csv")

# Cek apakah dataset berhasil dimuat
st.write("Kolom yang tersedia dalam dataset:", all_df.columns.tolist())

# Pastikan kolom yang dibutuhkan ada sebelum buat visualisasi
if 'payment_type' in all_df.columns:
    payment_df = all_df['payment_type'].value_counts().reset_index()
    payment_df.columns = ['payment_type', 'count']

    fig1 = px.bar(payment_df, x='payment_type', y='count', title='Number of Orders by Payment Method', text_auto=True)
    fig1.update_layout(yaxis_title='Number of Orders')

    st.plotly_chart(fig1)
else:
    st.error("Kolom 'payment_type' tidak ditemukan dalam dataset.")
