import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari GitHub
all_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/refs/heads/main/dashboard/all_data.csv")

# Pastikan data yang digunakan sesuai untuk masing-masing grafik
payment_df = all_df[['payment_type']].dropna()
review_df = all_df[['days_to_review']].dropna()

# Grafik 1: Bar chart metode pembayaran
st.title("Number of Orders by Payment Method")

fig1 = px.bar(payment_df, x='payment_type', title='Number of Orders by Payment Method', 
             labels={'payment_type': 'Payment Method', 'count': 'Number of Orders'}, 
             text_auto=True)

fig1.update_layout(yaxis_title='Number of Orders')

# Menampilkan plot di Streamlit
st.plotly_chart(fig1)

# Grafik 2: Histogram dengan KDE
st.title("Distribusi Waktu Pembuatan Review Setelah Barang Sampai")

# Data untuk histogram
hist_data = [review_df["days_to_review"].values]
group_labels = ["Days to Review"]

fig2 = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)

# Garis median
median_value = review_df["days_to_review"].median()
fig2.add_vline(x=median_value, line=dict(color="red", dash="dash"), name="Median")

# Label dan judul
fig2.update_layout(
    xaxis_title="Hari setelah barang sampai",
    yaxis_title="Density",
    legend_title="Legend"
)

# Tampilkan plot di Streamlit
st.plotly_chart(fig2)
