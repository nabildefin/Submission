import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

@st.cache_data
def load_data():
    datasets = {
        "Aotizhongxin": "PRSA_Data_Aotizhongxin_20130301-20170228.csv",
        "Changping": "PRSA_Data_Changping_20130301-20170228.csv",
        "Dingling": "PRSA_Data_Dingling_20130301-20170228.csv",
        "Dongsi": "PRSA_Data_Dongsi_20130301-20170228.csv",
        "Guanyuan": "PRSA_Data_Guanyuan_20130301-20170228.csv",
        "Gucheng": "PRSA_Data_Gucheng_20130301-20170228.csv",
        "Huairou": "PRSA_Data_Huairou_20130301-20170228.csv",
        "Nongzhanguan": "PRSA_Data_Nongzhanguan_20130301-20170228.csv",
        "Shunyi": "PRSA_Data_Shunyi_20130301-20170228.csv",
        "Tiantan": "PRSA_Data_Tiantan_20130301-20170228.csv",
        "Wanliu": "PRSA_Data_Wanliu_20130301-20170228.csv"
    }
    folder_path = "PRSA_Data_20130301-20170228"
    return {name: pd.read_csv(os.path.join(folder_path, file)) for name, file in datasets.items()}

# Load dataset
dataframes = load_data()

# Sidebar
st.sidebar.title("Dashboard Air Quality")
station_selected = st.sidebar.selectbox("Pilih Stasiun", list(dataframes.keys()))

df = dataframes[station_selected]

# Dashboard title
st.title("Dashboard Air Quality")

# Korelasi PM2.5 dengan faktor cuaca
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
weather_factors = ["PM2.5", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
korelasi_matrix = df[weather_factors].corr()
korelasi_PM25 = korelasi_matrix.loc["PM2.5"].drop("PM2.5").reset_index()
korelasi_PM25.columns = ["Cuaca", "Korelasi"]
st.dataframe(korelasi_PM25.set_index("Cuaca"))

# Heatmap korelasi
st.subheader("Heatmap Korelasi PM2.5 dengan Faktor Cuaca")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(korelasi_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
plt.title(f"Heatmap Korelasi di Stasiun {station_selected}")
st.pyplot(fig)

# Tren Rata-Rata Bulanan PM2.5
st.subheader("Tren Rata-Rata Bulanan PM2.5")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df_monthly_avg_PM25 = df.resample('M', on='datetime')['PM2.5'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_monthly_avg_PM25.index, df_monthly_avg_PM25.values, marker="o", linestyle="-", color="b")
ax.set_xlabel("Tanggal (Bulan)")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title(f"Rata-rata Bulanan PM2.5 di Stasiun {station_selected}")
plt.xticks(rotation=15)
plt.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)
