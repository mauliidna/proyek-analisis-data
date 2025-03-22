import streamlit as st
import pandas as pd
import plotly.express as px

# 📚 Load Data
def load_data():
    payment_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/refs/heads/main/order_payments_dataset.csv")
    review_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/refs/heads/main/order_reviews_dataset.csv")
    order_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/refs/heads/main/orders_dataset.csv")
    return payment_df, review_df, order_df

payment_df, review_df, order_df = load_data()

# ⏰ Pastikan kolom tanggal dalam format datetime
order_df["order_delivered_customer_date"] = pd.to_datetime(order_df["order_delivered_customer_date"], errors='coerce')
review_df["review_creation_date"] = pd.to_datetime(review_df["review_creation_date"], errors='coerce')

# 🔗 Merge review_df dengan order_df untuk mendapatkan order_delivered_customer_date
review_df = review_df.merge(order_df[["order_id", "order_delivered_customer_date"]], on="order_id", how="left")

# ✅ Buat kolom days_to_review jika belum ada
review_df["days_to_review"] = (review_df["review_creation_date"] - review_df["order_delivered_customer_date"]).dt.days

# 🔧 Bersihkan data: Hanya ambil nilai days_to_review yang >= 0 dan bukan NaN
review_df = review_df[(review_df["days_to_review"] >= 0) & (review_df["days_to_review"].notna())]

# 🌐 Streamlit App
st.set_page_config(layout="wide")
st.title("📊 Analisis Data E-Commerce")

# 🛍️ Layout dengan sidebar
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_payment_methods = st.multiselect("Pilih Metode Pembayaran", payment_df["payment_type"].unique(), default=payment_df["payment_type"].unique())
    min_days = int(review_df["days_to_review"].min())
    max_days = int(review_df["days_to_review"].max())
    days_range = st.slider("Pilih Rentang Hari untuk Review", min_value=min_days, max_value=max_days, value=(min_days, max_days))

# 🔍 Filter data
filtered_payment_df = payment_df[payment_df["payment_type"].isin(selected_payment_methods)]
filtered_review_df = review_df[(review_df["days_to_review"] >= days_range[0]) & (review_df["days_to_review"] <= days_range[1])]

# 🔄 Layout untuk visualisasi
st.subheader("💳 Metode Pembayaran yang Paling Sering Digunakan")
payment_counts = filtered_payment_df["payment_type"].value_counts().reset_index()
payment_counts.columns = ["payment_type", "count"]
fig = px.bar(payment_counts, x="payment_type", y="count", title="Number of Orders by Payment Method", labels={"payment_type": "Payment Method", "count": "Number of Orders"})
st.plotly_chart(fig)

with st.expander("🔎 Insight"):
    st.write("- Dari visualisasi di atas, kita dapat melihat metode pembayaran yang paling sering digunakan oleh pelanggan.")
    st.write("- Jika terdapat dominasi metode pembayaran tertentu, hal ini bisa menjadi peluang untuk meningkatkan kenyamanan transaksi pada metode tersebut.")
    st.write("- Jika metode pembayaran tertentu jarang digunakan, bisa jadi pelanggan kurang familiar atau terdapat kendala dalam penggunaannya.")
    st.write("- Menganalisis tren ini dapat membantu bisnis dalam menawarkan promo atau cashback pada metode pembayaran yang ingin lebih ditingkatkan penggunaannya.")

st.subheader("⏳ Waktu yang Dibutuhkan untuk Memberikan Ulasan")
fig2 = px.histogram(filtered_review_df, x="days_to_review", nbins=50, title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai", labels={"days_to_review": "Hari setelah barang sampai", "count": "Jumlah Review"})
fig2.update_yaxes(range=[0, 400000])  # Mengatur rentang jumlah review hingga 400000
fig2.add_vline(x=filtered_review_df["days_to_review"].median(), line_dash="dash", line_color="red", annotation_text="Median", annotation_position="top right")
st.plotly_chart(fig2)

with st.expander("🔎 Insight"):
    st.write("- Visualisasi ini menunjukkan sebaran waktu yang dibutuhkan pelanggan untuk memberikan ulasan setelah barang diterima.")
    st.write("- Jika mayoritas pelanggan memberikan ulasan dalam jangka waktu tertentu, maka strategi promosi atau reminder dapat difokuskan pada periode tersebut untuk meningkatkan engagement.")
    st.write("- Jika ada banyak pelanggan yang memberikan ulasan sangat lama setelah menerima barang, bisa jadi mereka hanya merespons ketika ada masalah dengan produk.")
    st.write("- Mengetahui pola ini dapat membantu dalam menentukan kapan sebaiknya pengingat ulasan dikirimkan untuk meningkatkan jumlah feedback pelanggan.")
