import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset hasil cleaning
url = "https://raw.githubusercontent.com/mauliidna/proyek-analisis-data/main/dashboard/all_data.csv"
all_df = pd.read_csv(url)

# Cek apakah dataset berhasil dimuat
st.write("Kolom yang tersedia dalam dataset:", all_df.columns.tolist())

# Plot 1: Bar Chart - Payment Type
if 'payment_type' in all_df.columns:
    payment_df = all_df['payment_type'].value_counts().reset_index()
    payment_df.columns = ['payment_type', 'count']

    fig1 = px.bar(payment_df, x='payment_type', y='count', title='Number of Orders by Payment Method', text_auto=True)
    fig1.update_layout(yaxis_title='Number of Orders')

    st.plotly_chart(fig1)
else:
    st.error("Kolom 'payment_type' tidak ditemukan dalam dataset.")

# Plot 2: Histogram - Days to Review
if 'days_to_review' in all_df.columns:
    fig2 = px.histogram(all_df, x="days_to_review", nbins=50, title="Distribusi Waktu Pembuatan Review Setelah Barang Sampai", 
                        marginal="box", opacity=0.7)
    
    # Tambahkan garis median
    median_value = all_df["days_to_review"].median()
    fig2.add_vline(x=median_value, line_dash="dash", line_color="red", annotation_text="Median", annotation_position="top left")

    fig2.update_layout(xaxis_title="Hari setelah barang sampai", yaxis_title="Jumlah Review")

    st.plotly_chart(fig2)
else:
    st.error("Kolom 'days_to_review' tidak ditemukan dalam dataset.")
