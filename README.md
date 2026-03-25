# 🌫️ Dashboard Kualitas Udara Beijing

Proyek analisis data kualitas udara Beijing menggunakan **Air Quality Dataset (PRSA)** yang mencakup data pengukuran per jam dari 12 stasiun pemantauan selama periode Maret 2013 – Februari 2017.

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Data bersih hasil proses wrangling
│   └── dashboard.py        # Aplikasi Streamlit
├── data/
│   ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
│   ├── PRSA_Data_Changping_20130301-20170228.csv
│   └── ... (12 file CSV)
├── notebook.ipynb          # Notebook analisis lengkap
├── requirements.txt        # Daftar dependensi Python
├── README.md               # File ini
└── url.txt                 # Tautan Streamlit Cloud (setelah deploy)
```

## 🔧 Cara Menjalankan Dashboard

### 1. Clone / Download Proyek

```bash
git clone <repo_url>
cd submission
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser pada alamat `http://localhost:8501`.

---

## 📊 Pertanyaan Bisnis yang Dijawab

1. **Bagaimana tren konsentrasi PM2.5 rata-rata per tahun dan per musim di seluruh stasiun?**
2. **Stasiun mana yang memiliki tingkat polusi tertinggi dan bagaimana perbandingannya?**

## 🔬 Analisis Lanjutan

- **Clustering berbasis Binning** — mengelompokkan pengamatan ke 6 kategori kualitas udara berdasarkan konsentrasi PM2.5 (standar AQI China).

## 📦 Library Utama

| Library | Kegunaan |
|---------|----------|
| pandas | Manipulasi data |
| numpy | Komputasi numerik |
| matplotlib | Visualisasi statis |
| seaborn | Visualisasi statistik |
| streamlit | Dashboard interaktif |
