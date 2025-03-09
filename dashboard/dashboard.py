import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    folder_path = "dashboard"  
    datasets = {
        "Aotizhongxin": f"{folder_path}/aotizhongxin_df.csv",
        "Changping": f"{folder_path}/changping_df.csv",
        "Dingling": f"{folder_path}/dingling_df.csv",
        "Dongsi": f"{folder_path}/dongsi_df.csv",
        "Guanyuan": f"{folder_path}/guanyuan_df.csv",
        "Gucheng": f"{folder_path}/gucheng_df.csv",
        "Huairou": f"{folder_path}/huairou_df.csv",
        "Nongzhanguan": f"{folder_path}/nongzhanguan_df.csv",
        "Shunyi": f"{folder_path}/shunyi_df.csv",
        "Tiantan": f"{folder_path}/tiantan_df.csv",
        "Wanliu": f"{folder_path}/wanliu_df.csv",
        "Wanshouxigong": f"{folder_path}/wanshouxigong_df.csv"
    }
    
    dataframes = {}
    for name, file_path in datasets.items():
        try:
            dataframes[name] = pd.read_csv(file_path)
        except FileNotFoundError:
            st.error(f"File {file_path} tidak ditemukan.")
    
    return dataframes


dataframes = load_data()

if not dataframes:
    st.error("Data tidak dapat dimuat. Pastikan file CSV ada di repositori GitHub dan path benar.")
else:
   
    st.sidebar.title("Dashboard Air Quality")
    station_selected = st.sidebar.selectbox("Pilih Stasiun", list(dataframes.keys()))

    df = dataframes[station_selected]

    st.title("Dashboard Air Quality")

    st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
    weather_factors = ["PM2.5", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
    
    if all(col in df.columns for col in weather_factors):
        korelasi_matrix = df[weather_factors].corr()
        korelasi_PM25 = korelasi_matrix.loc["PM2.5"].drop("PM2.5").reset_index()
        korelasi_PM25.columns = ["Cuaca", "Korelasi"]
        st.dataframe(korelasi_PM25.set_index("Cuaca"))

        
        st.subheader("Heatmap Korelasi PM2.5 dengan Faktor Cuaca")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(korelasi_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        plt.title(f"Heatmap Korelasi di Stasiun {station_selected}")
        st.pyplot(fig)
    else:
        st.error("Data tidak memiliki kolom yang sesuai untuk analisis korelasi.")

    if all(col in df.columns for col in ["year", "month", "day", "hour", "PM2.5"]):
        st.subheader("Tren Rata-Rata Bulanan PM2.5")
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df_monthly_avg_PM25 = df.resample('M', on='datetime')["PM2.5"].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df_monthly_avg_PM25.index, df_monthly_avg_PM25.values, marker="o", linestyle="-", color="b")
        ax.set_xlabel("Tanggal (Bulan)")
        ax.set_ylabel("Rata-rata PM2.5")
        ax.set_title(f"Rata-rata Bulanan PM2.5 di Stasiun {station_selected}")
        plt.xticks(rotation=15)
        plt.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)
    else:
        st.error("Data tidak memiliki kolom yang sesuai untuk analisis tren PM2.5.")
