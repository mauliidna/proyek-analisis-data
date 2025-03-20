import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# URL Dataset GitHub
base_url = "https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/refs/heads/main/"
df_order = pd.read_csv(base_url + "orders_dataset.csv")
df_review = pd.read_csv(base_url + "order_reviews_dataset.csv")
df_payments = pd.read_csv(base_url + "order_payments_dataset.csv")

# Gabungkan dataset berdasarkan 'order_id'
all_df = df_payments.merge(df_review, on="order_id").merge(df_order, on="order_id")

# Konversi ke datetime
all_df["order_delivered_customer_date"] = pd.to_datetime(all_df["order_delivered_customer_date"])
all_df["review_creation_date"] = pd.to_datetime(all_df["review_creation_date"])

# Hitung selisih waktu dalam hari antara review dan barang sampai (menghindari nilai negatif)
all_df["days_to_review"] = (all_df["review_creation_date"] - all_df["order_delivered_customer_date"]).dt.days.clip(lower=0)

# Sidebar Filter
st.sidebar.header("Filter Data")
payment_options = all_df["payment_type"].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options if payment_options.size > 0 else [])

day_min, day_max = int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", day_min, day_max, (day_min, day_max))

# Filter Data
filtered_df = all_df[(all_df["payment_type"].isin(selected_payment)) & (all_df["days_to_review"].between(*day_range))]

# 📊 Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran
fig_payment = px.bar(
    filtered_df["payment_type"].value_counts().reset_index(),
    x="index",
    y="payment_type",
    labels={"index": "Metode Pembayaran", "payment_type": "Jumlah Pesanan"},
    title="Jumlah Pesanan Berdasarkan Metode Pembayaran"
)

st.plotly_chart(fig_payment)

# ℹ️ Penjelasan Grafik Metode Pembayaran
with st.expander("ℹ️ Penjelasan Grafik: Number of Orders by Payment Method"):
    st.write("Grafik ini menunjukkan jumlah pesanan berdasarkan metode pembayaran yang digunakan oleh pelanggan.")
    st.markdown("**Insight:**")
    st.write("- **Kartu Kredit Dominan:** Mayoritas pesanan dibayar dengan kartu kredit.")
    st.write("- **Boleto sebagai Alternatif:** Metode pembayaran kedua yang paling banyak digunakan.")
    st.write("- **Kategori 'not_defined' Hampir Tidak Ada:** Mungkin terjadi karena kesalahan data atau metode pembayaran langka.")
    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Menawarkan insentif untuk metode pembayaran tertentu.")
    st.write("- Mengeksplorasi metode pembayaran lain seperti e-wallet.")

# 📊 Grafik 2: Distribusi Waktu Pembuatan Review Setelah Barang Sampai
fig_review = px.histogram(filtered_df, x="days_to_review", nbins=30, marginal="box", opacity=0.7)
fig_review.update_layout(
    title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai",
    xaxis_title="Hari setelah barang sampai",
    yaxis_title="Jumlah Review"
)

# Tambahkan Garis Median
median_value = filtered_df["days_to_review"].median()
fig_review.add_vline(x=median_value, line_dash="dash", line_color="red", annotation_text=f"Median: {median_value:.0f}")

st.plotly_chart(fig_review)

# ℹ️ Penjelasan Grafik Distribusi Review
with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review"):
    st.write("Grafik ini menunjukkan berapa lama waktu yang dibutuhkan pelanggan untuk memberikan review setelah menerima barang.")
    st.markdown("**Insight:**")
    st.write("- **Mayoritas Review Dibuat Cepat:** Banyak pelanggan memberikan review pada hari barang tiba.")
    st.write("- **Review Lama Setelah Barang Sampai (Outlier Positif):** Beberapa pelanggan menunggu lebih lama sebelum memberikan review.")
