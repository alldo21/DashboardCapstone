import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cardiovascular Disease Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('cardio_clean.csv')
    return df

try:
    df = load_data()

    st.sidebar.header("Filter Dashboard")
    
    min_age = int(df['age'].min())
    max_age = int(df['age'].max())
    age_range = st.sidebar.slider(
        "Pilih Rentang Usia:",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    gender_options = {1: "Perempuan", 2: "Laki-Laki"}
    selected_gender = st.sidebar.multiselect(
        "Pilih Gender:", 
        options=[1, 2], 
        default=[1, 2], 
        format_func=lambda x: gender_options[x]
    )

    filtered_df = df[
        (df['age'] >= age_range[0]) & 
        (df['age'] <= age_range[1]) & 
        (df['gender'].isin(selected_gender))
    ]

    st.title("📊 Cardiovascular Disease Analysis Dashboard")
    st.markdown("---")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Total Pasien", f"{len(filtered_df):,}")
    with col_m2:
        avg_val = filtered_df['age'].mean() if not filtered_df.empty else 0
        st.metric("Rata-rata Usia", f"{avg_val:.1f} Tahun")
    with col_m3:
        rel_val = (filtered_df['cardio'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Relevansi Penyakit", f"{rel_val:.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Korelasi Fitur Klinis")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        numeric_df = filtered_df.select_dtypes(include=[np.number])
        top_corr = numeric_df.corr()[['cardio']].sort_values(by='cardio', ascending=False)
        sns.heatmap(top_corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("2. Distribusi Tekanan Darah (Sistolik)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.kdeplot(data=filtered_df, x='ap_hi', hue='cardio', fill=True, palette='magma', ax=ax2)
        plt.legend(title='Kondisi', labels=['Sakit (1)', 'Sehat (0)'])
        st.pyplot(fig2)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("3. Risiko Berdasarkan Kelompok Usia")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        age_order = sorted(filtered_df['age_group'].unique())
        sns.barplot(data=filtered_df, x='age_group', y='cardio', order=age_order, palette='viridis', errorbar=None, ax=ax3)
        plt.ylabel("Persentase Risiko")
        st.pyplot(fig3)

    with col4:
        st.subheader("4. Perbandingan Risiko: Wanita vs Pria")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='gender', y='cardio', data=filtered_df, palette='Pastel1', errorbar=None, ax=ax4)
        ax4.set_xticklabels(['Wanita (1)', 'Pria (2)'])
        plt.ylabel("Persentase Risiko")
        st.pyplot(fig4)

    st.divider()

    st.subheader("5. Dampak Skor Gaya Hidup Tidak Sehat")
    st.info("Skor 0 (Sehat) hingga 3 (Sangat Tidak Sehat)")
    
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    sns.countplot(data=filtered_df, x='unhealthy_score', hue='cardio', palette='RdYlGn_r', ax=ax5)
    plt.legend(title='Kondisi', labels=['Sehat (0)', 'Sakit (1)'])
    
    for p in ax5.patches:
        ax5.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='center', xytext=(0, 7), textcoords='offset points')
    st.pyplot(fig5)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
st.caption("Copyright (c) Team CC26-PSU324 - Capstone Project 2026 - Analisis Penyakit Kardiovaskular")