import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari folder
base_url = "https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/refs/heads/main/"
order_df = pd.read_csv(base_url + "orders_dataset.csv")
review_df = pd.read_csv(base_url + "order_reviews_dataset.csv")
payment_df = pd.read_csv(base_url + "order_payments_dataset.csv")

# Gabungkan dataset berdasarkan 'order_id'
all_df = payment_df.merge(review_df, on="order_id").merge(order_df, on="order_id")

# Konversi ke datetime
all_df["order_delivered_customer_date"] = pd.to_datetime(all_df["order_delivered_customer_date"])
all_df["review_creation_date"] = pd.to_datetime(all_df["review_creation_date"])

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
payment_counts = filtered_df["payment_type"].value_counts()
fig_payment = px.bar(
    x=payment_counts.index,
    y=payment_counts.values,
    title="Jumlah Pesanan Berdasarkan Metode Pembayaran",
    labels={"x": "Metode Pembayaran", "y": "Jumlah Pesanan"}
)
st.plotly_chart(fig_payment)

# Grafik 2: Distribusi Waktu Pembuatan Review
fig_review_time = px.histogram(
    filtered_df,
    x="days_to_review",
    title="Distribusi Waktu Pembuatan Review",
    labels={"days_to_review": "Hari setelah barang sampai"},
    nbins=50 
)
st.plotly_chart(fig_review_time)
