import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari GitHub
url = "https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/main/dashboard/selected_data.csv"
all_df = pd.read_csv(url)

# Konversi ke datetime jika belum dilakukan
all_df["order_delivered_customer_date"] = pd.to_datetime(all_df["order_delivered_customer_date"], errors='coerce')
all_df["review_creation_date"] = pd.to_datetime(all_df["review_creation_date"], errors='coerce')

# Hitung selisih waktu dalam hari antara review dan barang sampai
all_df["days_to_review"] = (all_df["review_creation_date"] - all_df["order_delivered_customer_date"]).dt.days

# Hapus nilai negatif dari days_to_review
all_df = all_df[all_df["days_to_review"] >= 0]

# Sidebar Filter
st.sidebar.header("Filter Data")
payment_options = all_df["payment_type"].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options)
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max()), (int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())))

# Filter Data
filtered_df = all_df[(all_df["payment_type"].isin(selected_payment)) & (all_df["days_to_review"].between(day_range[0], day_range[1]))]

# Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran
st.subheader("Number of Orders by Payment Method")
payment_counts = filtered_df["payment_type"].value_counts()
payment_fig = px.bar(payment_counts, x=payment_counts.index, y=payment_counts.values, labels={'x': "Payment Method", 'y': "Number of Orders"}, title="Number of Orders by Payment Method")
st.plotly_chart(payment_fig)

# Grafik 2: Distribusi Waktu Pembuatan Review Setelah Barang Sampai
st.subheader("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")
days_fig = px.histogram(filtered_df, x="days_to_review", nbins=50, title="Distribusi Waktu Review", labels={'days_to_review': "Hari setelah barang sampai"})
st.plotly_chart(days_fig)
