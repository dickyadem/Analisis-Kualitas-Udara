import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
@st.cache_data
def load_data():
    data = pd.read_csv('PRSA_Data_Wanliu_20130301-20170228.csv')
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    data.set_index('datetime', inplace=True)
    return data

data = load_data()

st.title('Dashboard Analisis Kualitas Udara di Beijing (2013-2017)')
st.markdown('''Dashboard ini bertujuan untuk menganalisis tren kualitas udara dan faktor cuaca yang mempengaruhi tingkat polusi di Beijing.''')

st.sidebar.header('Filter Data')
year_filter = st.sidebar.slider('Pilih Tahun', 2013, 2017, (2013, 2017))
data_filtered = data[str(year_filter[0]):str(year_filter[1])]

st.subheader('Tren Tahunan PM2.5 dan PM10')
fig1, ax1 = plt.subplots()
data_filtered[['PM2.5', 'PM10']].resample('Y').mean().plot(ax=ax1, marker='o')
ax1.set_title('Annual Trends of PM2.5 and PM10')
ax1.set_xlabel('Year')
ax1.set_ylabel('Concentration (µg/m³)')
st.pyplot(fig1)

st.subheader('Tren Bulanan PM2.5 dan PM10')
fig2, ax2 = plt.subplots()
data_filtered[['PM2.5', 'PM10']].resample('M').mean().plot(ax=ax2)
ax2.set_title('Monthly Average Trends of PM2.5 and PM10')
ax2.set_xlabel('Date')
ax2.set_ylabel('Concentration (µg/m³)')
st.pyplot(fig2)

st.subheader('Korelasi antara PM2.5 dan Faktor Cuaca')
fig3, ax3 = plt.subplots(figsize=(10, 6))
corr = data_filtered[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax3)
ax3.set_title('Correlation Heatmap: PM2.5 vs Weather Factors')
st.pyplot(fig3)

st.subheader('Hubungan PM2.5 dengan Faktor Cuaca')
significant_factors = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for factor in significant_factors:
    fig, ax = plt.subplots()
    sns.regplot(x=factor, y='PM2.5', data=data_filtered, scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax)
    ax.set_title(f'PM2.5 vs {factor}')
    st.pyplot(fig)

 
st.subheader('Distribusi PM2.5 Berdasarkan Arah Angin')
fig4, ax4 = plt.subplots()
sns.boxplot(x='wd', y='PM2.5', data=data_filtered, palette='viridis', ax=ax4)
ax4.set_title('Distribution of PM2.5 by Wind Direction')
ax4.set_xlabel('Wind Direction')
ax4.set_ylabel('PM2.5 Concentration (µg/m³)')
st.pyplot(fig4)

# Informasi tambahan
st.markdown('---')
st.markdown('**Kesimpulan:**')
st.markdown('''
- Konsentrasi PM2.5 dan PM10 mengalami penurunan dari tahun ke tahun, terutama setelah 2014.
- Faktor cuaca seperti suhu (TEMP), tekanan udara (PRES), dan kecepatan angin (WSPM) memiliki pengaruh signifikan terhadap tingkat polusi udara.
- Konsentrasi PM2.5 lebih tinggi pada bulan-bulan musim dingin, menunjukkan pola musiman yang jelas.
''')
