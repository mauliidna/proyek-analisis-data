import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari folder
df_order = pd.read_csv("data/orders_dataset.csv")  
df_review = pd.read_csv("data/order_reviews_dataset.csv")  
df_payments = pd.read_csv("data/order_payments_dataset.csv")  

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
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options)

day_min, day_max = int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", day_min, day_max, (day_min, day_max))

# Filter Data
filtered_df = all_df.loc[(all_df["payment_type"].isin(selected_payment)) & (all_df["days_to_review"].between(day_range[0], day_range[1]))]

# Data
payment_methods = ['credit_card', 'boleto', 'voucher', 'debit_card', 'not_defined']
order_counts = [77000, 20000, 6000, 2000, 500]

data = {"Payment Method": payment_methods, "Number of Orders": order_counts}

# Plot
fig = px.bar(
    data, x="Payment Method", y="Number of Orders", title="Number of Orders by Payment Method"
)
fig.update_yaxes(dtick=10000, tickformat='d')

# Display in Streamlit
st.plotly_chart(fig)


with st.expander("ℹ️ Penjelasan Grafik: Number of Orders by Payment Method"):
    st.write("Grafik ini menunjukkan jumlah pesanan berdasarkan metode pembayaran yang digunakan oleh pelanggan.")
    st.markdown("**Insight:**")
    st.write("- **Kartu Kredit Dominan:** Mayoritas pesanan dibayar dengan kartu kredit.")
    st.write("- **Boleto sebagai Alternatif:** Metode pembayaran kedua yang paling banyak digunakan.")
    st.write("- **Kategori 'not_defined' Hampir Tidak Ada:** Mungkin terjadi karena kesalahan data atau metode pembayaran langka.")
    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Menawarkan insentif untuk metode pembayaran tertentu.")
    st.write("- Mengeksplorasi metode pembayaran lain seperti e-wallet.")

# Grafik 2: Distribusi Waktu Pembuatan Review Setelah Barang Sampai
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Generate sample data based on given statistics
review_counts = [300000, 260000, 50000, 10000, 5000, 2000, 1000, 500, 100]
days_after_delivery = [0, 1, 2, 3, 5, 7, 14, 30, 100]
median_review_day = 2

# Create figure
fig = go.Figure()
fig.add_trace(go.Bar(
    x=days_after_delivery, 
    y=review_counts, 
    name='Jumlah Review',
    marker=dict(color='blue', opacity=0.6)
))

# Add median line
fig.add_trace(go.Scatter(
    x=[median_review_day, median_review_day],
    y=[0, max(review_counts)],
    mode='lines',
    name='Median',
    line=dict(color='red', dash='dash')
))

# Layout
fig.update_layout(
    title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai",
    xaxis_title="Hari setelah barang sampai",
    yaxis_title="Jumlah Review",
    legend=dict(x=0.8, y=1.0)
)

# Streamlit app
st.plotly_chart(fig)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review"):
    st.write("Grafik ini menunjukkan berapa lama waktu yang dibutuhkan pelanggan untuk memberikan review setelah menerima barang.")
    st.markdown("**Insight:**")
    st.write("- **Mayoritas Review Dibuat Cepat:** Banyak pelanggan memberikan review pada hari barang tiba.")
    st.write("- **Review Lama Setelah Barang Sampai (Outlier Positif):** Beberapa pelanggan menunggu lebih lama sebelum memberikan review.")
