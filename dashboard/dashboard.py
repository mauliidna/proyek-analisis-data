import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Base URL file CSV di GitHub
base_url = "https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/main/"

# Baca dataset dari GitHub
order_df = pd.read_csv(base_url + "orders_dataset.csv")
payment_df = pd.read_csv(base_url + "order_payments_dataset.csv")
review_df = pd.read_csv(base_url + "order_reviews_dataset.csv")

# Merge data
order_df = order_df.merge(payment_df[['order_id', 'payment_value', 'payment_type']], on='order_id', how='left')
order_df = order_df.merge(review_df[['order_id', 'review_creation_date']], on='order_id', how='left')

# Konversi tanggal ke format datetime
order_df["order_delivered_customer_date"] = pd.to_datetime(order_df["order_delivered_customer_date"])
order_df["review_creation_date"] = pd.to_datetime(order_df["review_creation_date"])

# Hitung selisih hari antara review dan barang sampai
order_df["days_to_review"] = (order_df["review_creation_date"] - order_df["order_delivered_customer_date"]).dt.days

# Hapus nilai negatif
df = order_df[order_df["days_to_review"] >= 0]

# Sidebar Filter
st.sidebar.header("Filter Data")
payment_options = df["payment_type"].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", payment_options, default=payment_options)
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", int(df["days_to_review"].min()), int(df["days_to_review"].max()), (int(df["days_to_review"].min()), int(df["days_to_review"].max())))

# Filter Data
filtered_df = df[(df["payment_type"].isin(selected_payment)) & (df["days_to_review"].between(day_range[0], day_range[1]))]

# Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran
st.subheader("Number of Orders by Payment Method")
plt.figure(figsize=(8, 6))
sns.countplot(x='payment_type', data=payment_df)  # Menggunakan filtered_df di sini
plt.title('Number of Orders by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Number of Orders')
st.pyplot(plt)  # Mengganti plt.show() dengan st.pyplot()

with st.expander("ℹ️ Penjelasan Grafik: Number of Orders by Payment Method"):
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

# Menghitung days_to_review
df["days_to_review"] = (df["review_creation_date"] - df["order_delivered_customer_date"]).dt.days

# Menangani nilai negatif dengan mengatur nilai minimum ke 0
df["days_to_review"] = df["days_to_review"].clip(lower=0)

# Plot distribusi
plt.figure(figsize=(10, 5))
sns.histplot(df["days_to_review"], bins=50, kde=True)

# Garis median
plt.axvline(df["days_to_review"].median(), color='red', linestyle='dashed', linewidth=1, label='Median')

# Label dan judul
plt.xlabel("Hari setelah barang sampai")
plt.ylabel("Jumlah Review")
plt.title("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")
plt.legend()
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(plt)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review Setelah Barang Sampai"):
    st.write("Grafik ini menunjukkan distribusi waktu yang dibutuhkan pelanggan untuk memberikan review setelah barang diterima. Dengan melihat distribusi ini, kita dapat memahami seberapa cepat pelanggan memberikan feedback.")
    st.markdown("**Insight:**")
    st.write("- **Puncak di Awal:** Banyak pelanggan memberikan review dalam waktu singkat setelah menerima barang, menunjukkan kepuasan atau ketidakpuasan yang segera.")
    st.write("- **Beberapa Review Tertunda:** Ada juga pelanggan yang memberikan review setelah beberapa waktu, mungkin karena mereka ingin memastikan kualitas produk sebelum memberikan penilaian.")
    
    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Mengirimkan pengingat kepada pelanggan untuk memberikan review setelah beberapa hari menerima barang.")
    st.write("- Menyediakan insentif untuk review yang lebih cepat, seperti diskon untuk pembelian berikutnya.")
    st.write("- Menganalisis feedback dari review yang terlambat untuk memahami alasan di balik keterlambatan tersebut.")
