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

# Gabungkan dataset
all_df = pd.merge(order_df, payment_df, on='order_id', how='left')
all_df = pd.merge(all_df, review_df, on='order_id', how='left')

# Konversi kolom ke datetime
date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
             'order_delivered_customer_date', 'order_estimated_delivery_date', 'review_creation_date',
             'review_answer_timestamp']
for col in date_cols:
    all_df[col] = pd.to_datetime(all_df[col], errors='coerce')

# Hitung selisih waktu review dan filter nilai negatif
all_df['days_to_review'] = (all_df['review_creation_date'] - all_df['order_delivered_customer_date']).dt.days
all_df = all_df[all_df['days_to_review'] >= 0]

# Sidebar Filter
st.sidebar.header("Filter Data")
payment_options = all_df["payment_type"].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options)
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max()), (int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())))

# Filter Data
filtered_df = all_df[(all_df["payment_type"].isin(selected_payment)) & (all_df["days_to_review"].between(day_range[0], day_range[1]))]

# --- Visualisasi ---

# Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran
payment_data = {
    "payment_type": ["credit_card", "boleto", "voucher", "debit_card", "not_defined"],
    "count": [76795, 19784, 5775, 1529, 3]
}

# Convert to DataFrame
df = pd.DataFrame(payment_data)

# Streamlit App
st.title("Number of Orders by Payment Method")

# Create Bar Chart using Plotly
fig = px.bar(
    df, 
    x="payment_type", 
    y="count", 
    labels={"payment_type": "Payment Method", "count": "Number of Orders"},
    title="Number of Orders by Payment Method",
    color_discrete_sequence=["steelblue"]
)
fig.update_layout(yaxis_range=[0, 80000])

# Display Chart
st.plotly_chart(fig)
# Grafik 2: Distribusi Waktu Pembuatan Review
fig_review_time = px.histogram(
    filtered_df,
    x="days_to_review",
    title="Distribusi Waktu Pembuatan Review",
    labels={"days_to_review": "Hari setelah barang sampai"},
    nbins=50
)
st.plotly_chart(fig_review_time)
