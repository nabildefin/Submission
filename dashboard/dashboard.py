import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    datasets = {
        "Aotizhongxin": "aotizhongxin_df.csv",
        "Changping": "changping_df.csv",
        "Dingling": "dingling_df.csv",
        "Dongsi": "dongsi_df.csv",
        "Guanyuan": "guanyuan_df.csv",
        "Gucheng": "gucheng_df.csv",
        "Huairou": "huairou_df.csv",
        "Nongzhanguan": "nongzhanguan_df.csv",
        "Shunyi": "shunyi_df.csv",
        "Tiantan": "tiantan_df.csv",
        "Wanliu": "wanliu_df.csv",
        "Wanshouxigong": "wanshouxigong_df.csv"
    }
    return {name: pd.read_csv(file) for name, file in datasets.items()}

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
df_monthly_avg_PM25 = df.resample('M', on='datetime')["PM2.5"].mean()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_monthly_avg_PM25.index, df_monthly_avg_PM25.values, marker="o", linestyle="-", color="b")
ax.set_xlabel("Tanggal (Bulan)")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title(f"Rata-rata Bulanan PM2.5 di Stasiun {station_selected}")
plt.xticks(rotation=15)
plt.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)