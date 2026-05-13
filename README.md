# 📊 Cardiovascular Disease Analysis Dashboard

Dashboard interaktif ini dibangun menggunakan **Streamlit** untuk memvisualisasikan faktor-faktor risiko penyakit kardiovaskular. Proyek ini mencakup analisis korelasi fitur klinis, tren usia, perbandingan gender, hingga dampak gaya hidup terhadap kesehatan jantung.

## 🚀 Fitur Utama
* **Metrik Ringkasan**: Total pasien, rata-rata usia, dan persentase relevansi penyakit secara real-time.
* **Filter Interaktif**: Slider rentang usia dan filter gender pada sidebar untuk analisis yang lebih spesifik.
* **Visualisasi Data**:
    * Heatmap korelasi fitur klinis.
    * Distribusi tekanan darah (KDE Plot).
    * Tren risiko berdasarkan kelompok usia.
    * Perbandingan risiko antar gender.
    * Analisis skor gaya hidup tidak sehat.

## 📁 Struktur Folder
```text
CapstoneProject/
├── dashboard.py          # File utama aplikasi Streamlit
├── cardio_clean.csv      # Dataset utama yang sudah dibersihkan
├── requirements.txt      # Daftar library Python yang dibutuhkan
├── README.md             # Dokumentasi proyek
├── age_group.csv         # Dataset agregasi yang mengelompokkan rata-rata risiko berdasarkan rentang usia
├── correlation.csv       # Dataset Berisi matriks korelasi antar variabel numerik.
├── lifestyle.csv         # Dataset agregasi berdasarkan `unhealthy_score`
└── url.txt               # Link tautan akses ke dashboard streamlit


* **Cara Menjalankan**
- pip install -r requirements.txt
- streamlit run dashboard.py
