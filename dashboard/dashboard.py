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
# Data
payment_data = {
    "payment_type": ["credit_card", "boleto", "voucher", "debit_card", "not_defined"],
    "count": [76795, 19784, 5775, 1529, 3]
}

# Convert to DataFrame
df = pd.DataFrame(payment_data)

# Streamlit App
st.title("Number of Orders by Payment Method")

# Create Bar Chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(df["payment_type"], df["count"], color='steelblue')
ax.set_xlabel("Payment Method")
ax.set_ylabel("Number of Orders")
ax.set_title("Number of Orders by Payment Method")
ax.set_ylim(0, 80000)  # Adjusting the y-axis for better visualization
plt.xticks(rotation=0)

# Display Chart
st.pyplot(fig)


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
