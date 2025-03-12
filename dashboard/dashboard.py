import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis O3 di Shunyi Station")

file_path = "dashboard/main_data.csv"
main_data = pd.read_csv(file_path)

main_data["date"] = pd.to_datetime(main_data["date"], errors='coerce')
main_data = main_data.dropna(subset=["date"])

monthly_average_O3 = main_data.groupby(main_data["date"].dt.to_period("M"))["O3"].mean().reset_index()
monthly_average_O3["date"] = pd.to_datetime(monthly_average_O3["date"].dt.to_timestamp())

factor_df = main_data[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3","TEMP", "PRES", "DEWP", "WSPM", "RAIN"]].copy()

monthly_average_TEMP = main_data.groupby(main_data["date"].dt.to_period("M"))["TEMP"].mean().reset_index()
monthly_average_TEMP["date"] = pd.to_datetime(monthly_average_TEMP["date"].dt.to_timestamp())

monthly_average_O3_TEMP = monthly_average_O3.merge(monthly_average_TEMP, on= "date", how= "left")

st.subheader("Tren Rata-rata Kadar O3 di Shunyi Station")
fig1, ax1 = plt.subplots(figsize=(10,6))
sns.lineplot(data= monthly_average_O3,
             x= "date",
             y= "O3",
             linestyle= "-")
plt.xticks(rotation=15)
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Rata-rata kadar O3")
ax1.set_title("Tren Rata-rata O3")
plt.grid(linewidth = 0.2)
st.pyplot(fig1)

st.subheader("Korelasi kadar O3 dengan Faktor Pencemaran dan Faktor Cuaca di Shunyi Station")
correlation_matriks = factor_df.corr()[["O3"]].drop("O3")
fig2, ax2 = plt.subplots(figsize=(3, 6))
sns.heatmap(correlation_matriks, annot=True, cmap="coolwarm", fmt=".2f")
ax2.set_title("Korelasi Atribut lain dengan O3")
st.pyplot(fig2)

st.subheader("Hubungan Antara Kadar O3 dengan Temperatur")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_average_O3_TEMP,
             x="date",
             y="O3",
             label="O3")
sns.lineplot(data=monthly_average_O3_TEMP,
             x="date",
             y="TEMP",
             label="TEMP")
ax3.set_title("Hubungan Tren Rata-rata Kadar O3 dan TEMP di Shunyi Station")
ax3.set_xlabel("Tanggal")
ax3.set_ylabel("Rata-rata Kadar")
ax3.legend()
plt.grid(linewidth = 0.2)
st.pyplot(fig3)
