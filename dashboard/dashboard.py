import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 📚 Load Data
def load_data():
    all_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/refs/heads/main/dashboard/main_data.csv")
    return all_df

all_df = load_data()

# Plot distribusi
plt.figure(figsize=(10, 5))
sns.histplot(all_df["days_to_review"], bins=50, kde=True)

# 🌐 Streamlit App
st.set_page_config(layout="wide")
st.title("📊 Analisis Data E-Commerce")

# 🛍️ Layout dengan sidebar
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_payment_methods = st.multiselect("Pilih Metode Pembayaran", all_df["payment_type"].unique(), default=all_df["payment_type"].unique())
    min_days = int(all_df["days_to_review"].min())
    max_days = int(all_df["days_to_review"].max())
    days_range = st.slider("Pilih Rentang Hari untuk Review", min_value=min_days, max_value=max_days, value=(min_days, max_days))

# 🔍 Filter data
filtered_payment_df = all_df[all_df["payment_type"].isin(selected_payment_methods)]
filtered_review_df = all_df[(all_df["days_to_review"] >= days_range[0]) & (all_df["days_to_review"] <= days_range[1])]

# 🔄 Layout untuk visualisasi
st.subheader("💳 Metode Pembayaran yang Paling Sering Digunakan")
payment_counts = filtered_payment_df["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "count"]
fig = px.bar(payment_counts, x="payment_type", y="count", title="Number of Orders by Payment Method", labels={"payment_type": "Payment Method", "count": "Number of Orders"})
st.plotly_chart(fig)

with st.expander("🔎 Insight"):
    st.write("- Kartu Kredit Dominan: Mayoritas pesanan dibayar dengan kartu kredit, kemungkinan karena kemudahan transaksi dan fasilitas cicilan.")
    st.write("- Boleto sebagai Alternatif: Metode pembayaran populer kedua, digunakan oleh pelanggan tanpa kartu kredit atau yang lebih memilih pembayaran tunai.")
    st.write("- Voucher & Debit Card Kurang Populer: Digunakan dalam situasi tertentu seperti promo atau cashback.")
    st.write("- Kategori 'not_defined' Hampir Tidak Ada: Kemungkinan error data atau metode pembayaran yang jarang digunakan.")

st.subheader("⏳ Waktu yang Dibutuhkan untuk Memberikan Ulasan")
fig2 = px.histogram(all_df, x="days_to_review", nbins=50, title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai", labels={"days_to_review": "Hari setelah barang sampai", "count": "Jumlah Review"})
fig2.update_yaxes(range=[0, 400000])  
fig2.add_vline(x=all_df["days_to_review"].median(), line_dash="dash", line_color="red", annotation_text="Median", annotation_position="top right")
st.plotly_chart(fig2)

with st.expander("🔎 Insight"):
    st.write("- Mayoritas Review Dibuat Cepat: Sebagian besar pelanggan memberikan review pada hari barang tiba atau beberapa hari setelahnya.")
    st.write("- Review Sebelum Barang Sampai (Outlier Negatif): Bisa terjadi karena kesalahan sistem atau review dari pengalaman sebelumnya.")
    st.write("- Review Lama Setelah Barang Sampai (Outlier Positif): Beberapa pelanggan menunggu hingga mereka yakin atau setelah mendapat pengingat dari platform.")
    st.write("- Median 0 Hari: Setengah dari total review diberikan pada hari barang sampai, menunjukkan dorongan kuat dari notifikasi atau insentif e-commerce.")
