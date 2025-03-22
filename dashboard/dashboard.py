import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari GitHub
data_url = "https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/main/dashboard/all_data.csv"
all_df = pd.read_csv(data_url)

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
day_range = st.sidebar.slider("Rentang Waktu Review (hari)", int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max()), 
                              (int(all_df["days_to_review"].min()), int(all_df["days_to_review"].max())))

# Filter Data
filtered_df = all_df[(all_df["payment_type"].isin(selected_payment)) & 
                     (all_df["days_to_review"].between(day_range[0], day_range[1]))]

# ---- Grafik 1: Jumlah Pesanan Berdasarkan Metode Pembayaran ----
st.subheader("Number of Orders by Payment Method")

payment_counts = filtered_df["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "count"]

payment_fig = px.bar(payment_counts, x="payment_type", y="count", 
                     labels={"payment_type": "Payment Method", "count": "Number of Orders"}, 
                     title="Number of Orders by Payment Method", text_auto=True)

st.plotly_chart(payment_fig)

with st.expander("ℹ️ Penjelasan Grafik: Number of Orders by Payment Method"):
    st.write("Grafik ini menunjukkan jumlah pesanan berdasarkan metode pembayaran yang digunakan oleh pelanggan.")
    st.markdown("**Insight:**")
    st.write("- **Kartu Kredit Dominan:** Mayoritas pesanan dibayar dengan kartu kredit.")
    st.write("- **Boleto sebagai Alternatif:** Digunakan oleh pelanggan yang tidak memiliki kartu kredit.")
    st.write("- **Voucher & Debit Card Kurang Populer:** Biasanya digunakan dalam promo.")
    st.write("- **Kategori 'not_defined' Hampir Tidak Ada:** Bisa jadi karena kesalahan data.")
    
    st.markdown("**Potensi Tindakan Bisnis:**")
    st.write("- Menawarkan diskon untuk pembayaran selain kartu kredit.")
    st.write("- Mengeksplorasi metode pembayaran lain seperti e-wallet.")

# ---- Grafik 2: Distribusi Waktu Review ----
st.subheader("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")

days_fig = px.histogram(filtered_df, x="days_to_review", nbins=50, 
                        title="Distribusi Waktu Review", 
                        labels={"days_to_review": "Hari setelah barang sampai"},
                        marginal="box", opacity=0.7)

# Tambahkan garis median
median_value = filtered_df["days_to_review"].median()
days_fig.add_vline(x=median_value, line_dash="dash", line_color="red", 
                   annotation_text=f"Median: {median_value:.2f} hari", annotation_position="top left")

st.plotly_chart(days_fig)

with st.expander("ℹ️ Penjelasan Grafik: Distribusi Waktu Pembuatan Review"):
    st.write("Grafik ini menunjukkan berapa lama pelanggan butuh untuk memberikan review setelah menerima barang.")
    
    st.markdown("**Insight:**")
    st.write("- **Mayoritas Review Dibuat Cepat:** Banyak yang langsung review setelah barang sampai.")
    st.write("- **Beberapa Review Lama:** Bisa jadi mereka menunggu hingga yakin.")
    st.write("- **Median: 0 Hari** → Setengah dari review dibuat di hari yang sama.")
