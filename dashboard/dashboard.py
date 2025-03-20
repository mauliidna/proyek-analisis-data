import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
payment_counts = filtered_df['payment_type'].value_counts().reset_index()
payment_counts.columns = ['payment_type', 'order_count']

# Menggunakan Plotly untuk membuat bar chart
fig1 = px.bar(payment_counts, x='payment_type', y='order_count', 
               title='Number of Orders by Payment Method',
               labels={'payment_type': 'Payment Method', 'order_count': 'Number of Orders'},
               color='order_count', color_continuous_scale=px.colors.sequential.Viridis)

# Menampilkan plot di Streamlit
st.plotly_chart(fig1)

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

# Men angani nilai negatif dengan mengatur nilai minimum ke 0
filtered_df["days_to_review"] = filtered_df["days_to_review"].clip(lower=0)

# Plot distribusi menggunakan Plotly
fig2 = go.Figure()

# Histogram
fig2.add_trace(go.Histogram(x=filtered_df["days_to_review"], nbinsx=50, name='Jumlah Review', opacity=0.75))

# Garis median
median_value = filtered_df["days_to_review"].median()
fig2.add_trace(go.Scatter(x=[median_value, median_value], y=[0, filtered_df["days_to_review"].value_counts().max()], 
                           mode='lines', name='Median', line=dict(color='red', dash='dash')))

# Label dan judul
fig2.update_layout(title='Distribusi Waktu Pembuatan Review Setelah Barang Sampai',
                   xaxis_title='Hari setelah barang sampai',
                   yaxis_title='Jumlah Review',
                   bargap=0.2)

# Menampilkan plot di Streamlit
st.plotly_chart(fig2)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review Setelah Barang Sampai"):
    st.write("Grafik ini menunjukkan distribusi waktu yang dibutuhkan pelanggan untuk memberikan review setelah barang diterima. Garis median memberikan indikasi waktu rata-rata yang dihabiskan untuk memberikan review.")
    st.markdown("**Insight:**")
    st.write("- **Waktu Rata-rata:** Waktu median menunjukkan seberapa cepat pelanggan memberikan feedback setelah menerima produk.")
    st.write("- **Pentingnya Umpan Balik:** Memahami waktu ini dapat membantu dalam strategi pemasaran dan pengembangan produk.")
    st.write("- **Keterlambatan dalam Review:** Jika banyak review yang datang terlambat, mungkin ada masalah dalam pengalaman pelanggan yang perlu ditangani.")

    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Mendorong pelanggan untuk memberikan review lebih cepat melalui pengingat atau insentif.")
    st.write("- Menganalisis faktor-faktor yang menyebabkan keterlambatan dalam memberikan review untuk meningkatkan pengalaman pelanggan.")
