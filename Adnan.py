import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Set tema Streamlit
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Membaca data CSV dari GitHub
alldata_df = pd.read_csv("https://raw.githubusercontent.com/masadnan/submitionbangkit/main/all_data_ecommerce.csv")

# Header Streamlit dengan judul menarik
st.title('🛒 E-Commerce Dashboard')

# Menambahkan deskripsi untuk memberikan konteks
st.markdown(
    "Selamat datang di Dashboard E-Commerce! Pada Dashboard ini akan diberikan informasi terkait Hubungan ongkir dan berat barang, "
    "Persentase Tipe Pembayaran, dan Review customer."
)

# Membuat tab untuk subheader
selected_tab = st.sidebar.radio("Pilih Menu", ["Hubungan", "Persentase Tipe Pembayaran", "Review Customer"])

if selected_tab == "Hubungan":
    st.subheader("Hubungan")

    # Melihat korelasi antara price dan freight_value
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 6))
    sns.regplot(x=alldata_df['product_weight_g'], y=alldata_df['freight_value'], ax=ax)
    st.pyplot(fig)

    # Membuat heatmap untuk matriks korelasi
    selected_columns = alldata_df[['freight_value','product_weight_g']]
    correlation_mat = selected_columns.corr()
    sns.heatmap(correlation_mat, annot=True, cmap='GnBu', fmt='.2f', linewidths=0.1)
    st.pyplot()

# Tab "Persentase Tipe Pembayaran"
elif selected_tab == "Persentase Tipe Pembayaran":
    st.subheader("Persentase Tipe Pembayaran")

    # Menentukan persentase tipe payment yang digunakan
    payment_count = alldata_df['payment_type'].value_counts()
    plt.pie(
        x=payment_count,
        labels=payment_count.index,
        autopct='%1.1f%%',
        colors=sns.color_palette("deep", len(payment_count)),
        explode=(0.1, 0, 0, 0)
    )
    st.pyplot()

# Tab "Review Customer"
elif selected_tab == "Review Customer":
    st.subheader("Review Customer")

    # Menentukan proporsi penilaian customer
    bycategory_df = alldata_df.groupby(by=["review_score"]).order_id.nunique().reset_index()
    bycategory_df.rename(columns={"order_id": "cust_count"}, inplace=True)

    plt.figure(figsize=(10, 5))
    sns.barplot(
        y="cust_count",
        x="review_score",
        hue="cust_count",
        data=bycategory_df.sort_values(by="cust_count", ascending=False),
        palette="viridis", legend=False
    )
    st.pyplot()

st.caption("Copyright by AdnanSyawal")
