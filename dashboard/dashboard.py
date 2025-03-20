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
import streamlit as st
import pandas as pd
import plotly.express as px

# Data
data = {
    "days_after_delivery": [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
        21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 38, 43, 44, 45, 46, 47, 48, 50, 
        51, 52, 55, 56, 59, 66, 88, 106
    ],
    "review_count": [
        98074, 1079, 341, 145, 129, 134, 116, 119, 84, 48, 45, 44, 46, 21, 32, 32, 
        12, 21, 22, 12, 16, 7, 9, 8, 3, 1, 2, 2, 4, 3, 2, 1, 2, 2, 1, 1, 1, 4, 1, 
        1, 1, 2, 1, 1, 2, 1, 1, 12
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate median
median_value = df["days_after_delivery"].median()

# Streamlit App
st.title("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")

# Create Bar Chart using Plotly
fig = px.bar(
    df, 
    x="days_after_delivery", 
    y="review_count", 
    labels={"days_after_delivery": "Hari setelah barang sampai", "review_count": "Jumlah Review"},
    title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai",
    color_discrete_sequence=["steelblue"]
)

# Add Median Line
fig.add_vline(
    x=median_value, 
    line_dash="dash", 
    line_color="red", 
    annotation_text=f"Median ({median_value})", 
    annotation_position="top right"
)

# Display Chart
st.plotly_chart(fig)
