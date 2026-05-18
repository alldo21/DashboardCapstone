import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cardiovascular Dashboard", layout="wide")

sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    return pd.read_csv('cardio_clean.csv')

try:
    df = load_data()

    st.sidebar.header("Filter Dashboard")
    age_range = st.sidebar.slider("Rentang Usia:", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
    selected_gender = st.sidebar.multiselect("Gender:", [1, 2], [1, 2], format_func=lambda x: "Wanita" if x==1 else "Pria")

    filtered_df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1]) & (df['gender'].isin(selected_gender))].copy()

    st.title("📊 Cardiovascular Disease Dashboard")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Pasien", f"{len(filtered_df):,}")
    with m2:
        st.metric("Rata-rata Usia", f"{filtered_df['age'].mean():.1f} Tahun" if not filtered_df.empty else "0")
    with m3:
        rel = (filtered_df['cardio'].mean() * 100) if not filtered_df.empty else 0
        st.metric("Relevansi Penyakit", f"{rel:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Korelasi Fitur Terhadap Risiko Kardiovaskular")
        if not filtered_df.empty:
            numeric_df = filtered_df.select_dtypes(include=[np.number])
                
            pearson_corr = numeric_df.corr(method='pearson')[['cardio']].rename(columns={'cardio': 'Pearson'})
            spearman_corr = numeric_df.corr(method='spearman')[['cardio']].rename(columns={'cardio': 'Spearman'})
            
            top_corr = pearson_corr.join(spearman_corr).drop('cardio').sort_values(by='Spearman', ascending=False)
            
            fig1, ax1 = plt.subplots(figsize=(6, 10))
            sns.heatmap(top_corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-0.5, vmax=0.5, ax=ax1, cbar=True)
            st.pyplot(fig1)
        else:
            st.warning("Data kosong untuk filter korelasi.")

    with col2:
        st.subheader("2. Perbandingan Distribusi Tekanan Darah Sistolik")
        if not filtered_df.empty:
            fig2, ax2 = plt.subplots(figsize=(10, 8.5))
            sns.kdeplot(data=filtered_df, x='ap_hi', hue='cardio', fill=True, common_norm=False, palette='magma', alpha=0.5, ax=ax2)
            plt.xlabel("Tekanan Darah Sistolik (mmHg)")
            plt.ylabel("Kepadatan Data (Density)")
            plt.legend(title='Kondisi', labels=['Berisiko (1)', 'Sehat (0)'])
            st.pyplot(fig2)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("3. Risiko Berdasarkan Kelompok Usia")
        age_risk = filtered_df.groupby('age_group', observed=True)['cardio'].mean().reset_index()
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=age_risk, x='age_group', y='cardio', palette='viridis', ax=ax3)
        ax3.set_ylabel("Tingkat Risiko (0-1)")
        st.pyplot(fig3)

    with col4:
        st.subheader("4. Perbandingan Risiko: Wanita vs Pria")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=filtered_df, x='gender', y='cardio', palette='Pastel1', errorbar=None, ax=ax4)
        ax4.set_xticklabels(['Wanita (1)', 'Pria (2)'])
        st.pyplot(fig4)

    st.divider()

    st.subheader("5. Dampak Skor Gaya Hidup Tidak Sehat (%)")
    if not filtered_df.empty:
        df_plot = filtered_df.groupby(['unhealthy_score', 'cardio']).size().reset_index(name='count')
        total_counts = filtered_df.groupby('unhealthy_score').size().reset_index(name='total')
        df_plot = df_plot.merge(total_counts, on='unhealthy_score')
        df_plot['percentage'] = (df_plot['count'] / df_plot['total']) * 100

        fig5, ax5 = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_plot, x='unhealthy_score', y='percentage', hue='cardio', palette='RdYlGn_r', ax=ax5)
        
        for p in ax5.patches:
            height = p.get_height()
            if height > 0:
                ax5.annotate(f'{height:.1f}%', (p.get_x() + p.get_width() / 2, height + 1), ha='center', fontweight='bold', size=9)

        plt.legend(title='Kondisi', labels=['Sehat (0)', 'Sakit (1)'])
        plt.ylabel("Persentase (%)")
        plt.ylim(0, 110)
        st.pyplot(fig5)

except Exception as e:
    st.error(f"Terjadi kesalahan sistem: {e}")
st.caption("Copyright (c) Team CC26-PSU324 - Capstone Project 2026 - Analisis Penyakit Kardiovaskular")
