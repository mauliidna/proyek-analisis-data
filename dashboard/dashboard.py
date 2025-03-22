import streamlit as st
import pandas as pd
import plotly.express as px

# Judul Dashboard
st.subheader("MC009D5X2352 | Mauldina Rahmawati")
st.title("Dashboard Analisis Review dan Pembayaran")

# Load dataset dari folder
all_df = pd.read_csv("https://raw.githubusercontent.com/mauliidna/data-data-proyek-analisis-data-python/dashboard/main_data.csv")

# grafik 1
st.title("Number of Orders by Payment Method")

# Membuat bar chart
fig = px.bar(payment_df, x='payment_type', title='Number of Orders by Payment Method', 
             labels={'payment_type': 'Payment Method', 'count': 'Number of Orders'}, 
             text_auto=True)

fig.update_layout(yaxis_title='Number of Orders')

# Menampilkan plot di Streamlit
st.plotly_chart(fig)

#grafik 2
# Membuat histogram dengan KDE
fig = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)

# Garis median
median_value = merged_df["days_to_review"].median()
fig.add_vline(x=median_value, line=dict(color="red", dash="dash"), name="Median")

# Label dan judul
fig.update_layout(
    xaxis_title="Hari setelah barang sampai",
    yaxis_title="Density",
    legend_title="Legend"
)

# Tampilkan plot di Streamlit
st.plotly_chart(fig)


