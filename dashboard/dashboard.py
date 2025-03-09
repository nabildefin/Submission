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
    dataframes = {name: pd.read_csv(os.path.join(folder_path, file)) for name, file in datasets.items()}
    return dataframes

dataframes = load_data()

st.sidebar.title("Dashboard Air Quality")
option = st.sidebar.selectbox("Pilih Station", list(dataframes.keys()))

df = dataframes[option]

st.write("# Dashboard Air Quality")
st.write("### Korelasi PM2.5 dengan Faktor Cuaca")
df_PM25_cuaca = df[["PM2.5", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]]
korelasi_matrix = df_PM25_cuaca.corr()
korelasi_long = korelasi_matrix.reset_index().melt(id_vars="index")
korelasi_long.columns = ["Polutan", "Cuaca", "Correlation"]
PM25_correlation = korelasi_long[korelasi_long["Polutan"] == "PM2.5"]
st.write(PM25_correlation.set_index("Cuaca"))

st.write("### Heatmap Korelasi PM2.5 dengan Faktor Cuaca")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(korelasi_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
plt.title(f"Heatmap Korelasi di Stasiun {option}", fontsize=16)
st.pyplot(fig)

st.write("### Tren Rata-Rata Bulanan PM2.5")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df_monthly_avg_PM25 = df.resample('M', on='datetime')['PM2.5'].mean()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_monthly_avg_PM25.index, df_monthly_avg_PM25.values, marker="o", linestyle="-", color="b")
ax.set_xlabel("Date (Month)", fontsize=15)
ax.set_ylabel("Average PM2.5", fontsize=15)
ax.set_title(f"Monthly Average PM2.5 at {option} Station", fontsize=20)
plt.xticks(rotation=15)
plt.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)