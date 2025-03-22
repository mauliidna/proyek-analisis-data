import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari GitHub (sudah bersih)
data_url = "https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/main/dashboard/all_data.csv"
all_df = pd.read_csv(data_url)

# Sidebar Filter
st.sidebar.header("Filter Data")
payment_options = all_df["payment_type"].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options)

# Pastikan kolom days_to_review ada dan tidak negatif
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max()), 
                              (int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())))

# Filter Data
filtered_df = all_df[(all_df["payment_type"].isin(selected_payment)) & 
                     (all_df["days_to_review"].between(day_range[0], day_range[1]))]

# ---- Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran ----
st.subheader("Number of Orders by Payment Method")

payment_counts = filtered_df["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "count"]

payment_fig = px.bar(payment_counts, x="payment_type", y="count", 
                     labels={"payment_type": "Payment Method", "count": "Number of Orders"}, 
                     title="Number of Orders by Payment Method", text_auto=True)

st.plotly_chart(payment_fig)

# ---- Grafik 2: Distribusi Waktu Review ----
st.subheader("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")

days_fig = px.histogram(filtered_df, x="days_to_review", nbins=50, 
                        title="Distribusi Waktu Review", 
                        labels={"days_to_review": "Hari setelah barang sampai"},
                        marginal="box", opacity=0.7)

# Tambahkan garis median
median_value = filtered_df["days_to_review"].median()
days_fig.add_vline(x=median_value, line_dash="dash", line_color="red", 
                   annotation_text=f"Median: {median_value:.2f} hari", annotation_position="top left")

st.plotly_chart(days_fig)
