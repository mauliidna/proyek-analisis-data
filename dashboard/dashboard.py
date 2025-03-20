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
payment_counts = payment_df["payment_type"].value_counts()
payment_fig = px.bar(payment_counts, x=payment_counts.index, y=payment_counts.values, labels={'x': "Payment Method", 'y': "Number of Orders"}, title="Number of Orders by Payment Method")
st.plotly_chart(payment_fig)

with st.expander("ℹ️ Penjelasan Grafik: Number of Orders by Payment Method "):
    st.write("Grafik ini menunjukkan jumlah pesanan berdasarkan metode pembayaran yang digunakan oleh pelanggan. Dari sini, kita dapat melihat metode pembayaran yang paling populer serta perbandingannya dengan metode lain.")
    st.markdown("**Insight:**")
    st.write("- **Kartu Kredit Dominan:** Mayoritas pesanan dibayar dengan kartu kredit, kemungkinan karena kemudahan transaksi dan fasilitas cicilan.")
    st.write("- **Boleto sebagai Alternatif:** Metode pembayaran populer kedua, digunakan oleh pelanggan yang tidak memiliki kartu kredit atau lebih memilih pembayaran tunai.")
    st.write("- **Voucher & Debit Card Kurang Populer:** Biasanya digunakan dalam situasi tertentu seperti promo atau cashback.")
    st.write("- **Kategori 'not_defined' Hampir Tidak Ada:** Mungkin terjadi karena kesalahan data atau metode pembayaran yang sangat jarang digunakan.")
    
    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Menawarkan insentif untuk pembayaran non-kartu kredit, seperti diskon untuk boleto.")
    st.write("- Mendorong penggunaan kartu kredit untuk mempercepat transaksi.")
    st.write("- Mengeksplorasi metode pembayaran lain seperti e-wallet untuk menarik lebih banyak pelanggan.")

# Grafik 2: Distribusi Waktu Pembuatan Review Setelah Barang Sampai
st.subheader("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")
days_fig = px.histogram(filtered_df, x="days_to_review", nbins=50, title="Distribusi Waktu Review", labels={'days_to_review': "Hari setelah barang sampai"})
st.plotly_chart(days_fig)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review"):
    st.write("Grafik ini menunjukkan berapa lama waktu yang dibutuhkan pelanggan untuk memberikan review setelah mereka menerima barangnya. Dari pola distribusi, kita bisa memahami kebiasaan pelanggan dalam memberikan feedback.")
    
    st.markdown("**Insight:**")
    st.write("- **Mayoritas Review Dibuat Cepat:** Sebagian besar pelanggan memberikan review pada hari barang tiba atau beberapa hari setelahnya.")
    st.write("- **Review Lama Setelah Barang Sampai (Outlier Positif):** Beberapa pelanggan menunggu hingga mereka benar-benar yakin atau setelah menerima pengingat dari platform.")
    st.write("- **Median 0 Hari:** Setengah dari total review diberikan pada hari barang sampai, menunjukkan adanya dorongan kuat dari notifikasi atau insentif dari e-commerce.")
