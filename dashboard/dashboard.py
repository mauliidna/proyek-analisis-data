import pandas as pd
import plotly.express as px

# Baca dataset
order_df = pd.read_csv("order_data.csv")
payment_df = pd.read_csv("payment_data.csv")
review_df = pd.read_csv("review_data.csv")

# Merge data
order_df = order_df.merge(payment_df[['order_id', 'payment_value', 'payment_type']], on='order_id', how='left')
order_df = order_df.merge(review_df[['order_id', 'review_creation_date']], on='order_id', how='left')

# Konversi tanggal ke format datetime
order_df["order_delivered_customer_date"] = pd.to_datetime(order_df["order_delivered_customer_date"])
order_df["review_creation_date"] = pd.to_datetime(order_df["review_creation_date"])

# Hitung selisih hari antara review dan barang sampai
order_df["days_to_review"] = (order_df["review_creation_date"] - order_df["order_delivered_customer_date"]).dt.days

# Hapus nilai negatif
order_df = order_df[order_df["days_to_review"] >= 0]

# Kategorisasi harga
bins = [0, 50, 100, 200, 500, 1000, 5000, 10000]
labels = ["<50", "50-100", "100-200", "200-500", "500-1000", "1000-5000", ">5000"]
order_df["price_range"] = pd.cut(order_df["payment_value"], bins=bins, labels=labels)

# Visualisasi metode pembayaran berdasarkan rentang harga
fig_payment = px.bar(order_df, x="price_range", color="payment_type", barmode="stack", opacity=0.8,
                     title="Metode Pembayaran Berdasarkan Rentang Harga Barang",
                     labels={"price_range": "Rentang Harga", "payment_type": "Metode Pembayaran"})
fig_payment.show()

# Visualisasi distribusi waktu pembuatan review
fig_review = px.histogram(order_df, x="days_to_review", nbins=50, title="Distribusi Waktu Review Setelah Barang Sampai",
                          labels={"days_to_review": "Hari setelah barang sampai"})
fig_review.show()
