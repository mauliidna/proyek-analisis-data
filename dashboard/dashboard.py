import streamlit as st
import pandas as pd
import plotly.express as px

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
payment_counts = filtered_df["payment_type"].value_counts().reset_index()
payment_counts.columns = ['payment_type', 'order_count']

# Menggunakan Plotly untuk membuat bar chart
fig = px.bar(payment_counts, x='payment_type', y='order_count', title='Number of Orders by Payment Method',
              labels={'payment_type': 'Payment Method', 'order_count': 'Number of Orders'},
              color='order_count', color_continuous_scale=px.colors.sequential.Viridis)

# Menampilkan plot di Streamlit
st.plotly_chart(fig)

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
# Plot distribusi
fig2 = px.histogram(df, x="days_to_review", nbins=50, title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai",
                     labels={'days_to_review': 'Hari setelah barang sampai'},
                     histnorm='count')

# Menambahkan median_line = df["days_to_review"].median()
fig2.add_vline(x=median_line, line_color='red', line_dash='dash', annotation_text='Median', annotation_position='top right')

# Menampilkan plot di Streamlit
st.plotly_chart(fig2)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review Setelah Barang Sampai"):
    st.write("Grafik ini menunjukkan distribusi waktu yang dibutuhkan pelanggan untuk memberikan review setelah barang diterima. Dari sini, kita dapat melihat pola dan kecenderungan dalam waktu pembuatan review.")
    st.markdown("**Insight:**")
    st.write("- **Waktu Pembuatan Review Bervariasi:** Beberapa pelanggan memberikan review segera setelah menerima barang, sementara yang lain mungkin membutuhkan waktu lebih lama.")
    st.write("- **Median Waktu:** Garis median menunjukkan waktu rata-rata yang dihabiskan pelanggan untuk memberikan review.")
    st.write("- **Pentingnya Umpan Balik:** Memahami waktu pembuatan review dapat membantu dalam strategi pemasaran dan pengembangan produk.")

    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Mendorong pelanggan untuk memberikan review lebih cepat melalui pengingat atau insentif.")
    st.write("- Menganalisis faktor-faktor yang mempengaruhi waktu pembuatan review untuk meningkatkan pengalaman pelanggan.")
