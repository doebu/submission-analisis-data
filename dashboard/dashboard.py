import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Kualitas Udara Beijing",
    page_icon="🌫️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv", parse_dates=["datetime"])
    return df

df = load_data()

season_order = ["Winter", "Spring", "Summer", "Autumn"]
quality_order = ["Baik", "Sedang", "Tidak Sehat (Sensitif)", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"]
quality_colors = ["#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#8e44ad", "#2c3e50"]
season_colors = {"Winter": "#3498db", "Spring": "#2ecc71", "Summer": "#f39c12", "Autumn": "#e67e22"}

st.sidebar.title("🌫️ Filter Data")
all_stations = sorted(df["station"].unique())
selected_stations = st.sidebar.multiselect("Pilih Stasiun:", all_stations, default=all_stations)
year_range = st.sidebar.slider("Rentang Tahun:", int(df["year"].min()), int(df["year"].max()), (int(df["year"].min()), int(df["year"].max())))

df_filter = df[(df["station"].isin(selected_stations)) &
               (df["year"] >= year_range[0]) &
               (df["year"] <= year_range[1])]

st.title("🌫️ Dashboard Kualitas Udara Beijing (2013–2017)")
st.caption("Sumber: PRSA Air Quality Dataset | Visualisasi Interaktif")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Rata-rata PM2.5", f"{df_filter['PM2.5'].mean():.1f} µg/m³")
with c2:
    st.metric("PM2.5 Tertinggi", f"{df_filter['PM2.5'].max():.0f} µg/m³")
with c3:
    station_worst = df_filter.groupby("station")["PM2.5"].mean().idxmax()
    st.metric("Stasiun Terpolusi", station_worst)
with c4:
    station_best = df_filter.groupby("station")["PM2.5"].mean().idxmin()
    st.metric("Stasiun Terbersih", station_best)

st.divider()

st.subheader("📅 Pertanyaan 1: Pada tahun dan musim apa rata-rata PM2.5 tertinggi terjadi di Beijing selama Maret 2013 – Februari 2017?")
col1, col2 = st.columns(2)

with col1:
    yearly_mean = df_filter.groupby("year")["PM2.5"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    bar_colors = ["#e74c3c" if v > 75 else "#2ecc71" for v in yearly_mean["PM2.5"]]
    bars = ax.bar(yearly_mean["year"].astype(str), yearly_mean["PM2.5"],
                  color=bar_colors, edgecolor="white", width=0.55)
    ax.axhline(75, color="orange", linestyle="--", linewidth=1.5, label="Ambang (75 µg/m³)")
    ax.axhline(15, color="green", linestyle=":", linewidth=1.5, label="Standar WHO (15 µg/m³)")
    for bar, val in zip(bars, yearly_mean["PM2.5"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Tahun"); ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_title("Rata-rata PM2.5 per Tahun (2013–2017)", fontweight="bold")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with col2:
    seasonal_mean = df_filter.groupby("season")["PM2.5"].mean().reindex(season_order).reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    bars2 = ax.bar(seasonal_mean["season"], seasonal_mean["PM2.5"],
                   color=[season_colors.get(s, "#999") for s in seasonal_mean["season"]],
                   edgecolor="white", width=0.55)
    ax.axhline(75, color="orange", linestyle="--", linewidth=1.5, label="Ambang (75 µg/m³)")
    for bar, val in zip(bars2, seasonal_mean["PM2.5"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Musim"); ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_title("Rata-rata PM2.5 per Musim (2013–2017)", fontweight="bold")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with st.expander("📝 Insight Pertanyaan 1"):
    st.write("""
    - Selama periode **Maret 2013 – Februari 2017**, **tahun 2013** mencatat rata-rata PM2.5 tertinggi di antara seluruh tahun pengamatan.
    - Terdapat tren **penurunan dari 2013 hingga 2016**, mengindikasikan dampak positif kebijakan pengendalian polusi, namun angka sedikit meningkat kembali pada 2017.
    - Seluruh tahun **melampaui ambang batas China (75 µg/m³)** dan jauh di atas standar WHO (15 µg/m³).
    - Secara musiman, **Winter (musim dingin)** secara konsisten mencatat rata-rata PM2.5 **tertinggi** akibat meningkatnya penggunaan pemanas berbahan bakar batu bara.
    - **Summer (musim panas)** mencatat rata-rata PM2.5 **terendah** berkat curah hujan yang lebih tinggi dan angin yang lebih kencang.
    """)

st.divider()

st.subheader("📍 Pertanyaan 2: Stasiun mana yang memiliki rata-rata PM2.5 tertinggi dan terendah, serta berapa besar selisihnya selama Maret 2013 – Februari 2017?")
col3, col4 = st.columns(2)

with col3:
    station_mean = df_filter.groupby("station")["PM2.5"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    palette = ["#e74c3c" if v > 75 else "#3498db" for v in station_mean.values]
    bars3 = ax.barh(station_mean.index, station_mean.values, color=palette,
                    edgecolor="white", height=0.65)
    ax.axvline(75, color="orange", linestyle="--", linewidth=1.5, label="Ambang (75 µg/m³)")
    for bar, val in zip(bars3, station_mean.values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
    ax.set_title("Rata-rata PM2.5 per Stasiun (Maret 2013 – Februari 2017)", fontweight="bold")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with col4:
    station_order_box = df_filter.groupby("station")["PM2.5"].mean().sort_values(ascending=False).index.tolist()
    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot([df_filter[df_filter["station"] == s]["PM2.5"].dropna().values for s in station_order_box],
                    vert=True, patch_artist=True, showfliers=False,
                    medianprops=dict(color="black", linewidth=2))
    cmap_colors = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(station_order_box)))
    for patch, color in zip(bp["boxes"], cmap_colors):
        patch.set_facecolor(color); patch.set_alpha(0.85)
    ax.set_xticklabels(station_order_box, rotation=45, ha="right", fontsize=8)
    ax.axhline(75, color="orange", linestyle="--", linewidth=1.5, label="Ambang (75 µg/m³)")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_title("Distribusi PM2.5 per Stasiun (Maret 2013 – Februari 2017)", fontweight="bold")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

with st.expander("📝 Insight Pertanyaan 2"):
    best = df_filter.groupby("station")["PM2.5"].mean().idxmin()
    worst = df_filter.groupy("station")["PM2.5"].mean().idxmax()
    best_val = df_filter.groupby("station")["PM2.5"].mean().min()
    worst_val = df_filter.groupby("station")["PM2.5"].mean().max()
    selisih = worst_val - best_val
    st.write("""
    - Selama periode **Maret 2013 – Februari 2017**, stasiun **{worst}** mencatat rata-rata PM2.5 **tertinggi** ({worst_val:.1f} µg/m³), sementara stasiun **{best}** mencatat rata-rata PM2.5 **terendah** ({best_val:.1f} µg/m³).
    - **Selisih rata-rata PM2.5** antara stasiun terpolusi dan terbersih adalah **{selisih:.1f} µg/m³**, mencerminkan pengaruh signifikan lokasi geografis (pusat kota/industri vs pinggiran/pegunungan).
    - Meskipun demikian, **semua stasiun** rata-rata tetap melampaui ambang batas China 75 µg/m³ selama periode pengamatan.
    """)

st.divider()

st.subheader("🔬 Analisis Lanjutan: Clustering Kualitas Udara (Binning)")
st.write("Setiap pengamatan dikategorikan berdasarkan konsentrasi PM2.5 mengikuti standar AQI China.")

sq = df_filter.groupby(["station", "air_quality"]).size().unstack(fill_value=0)
sq = sq.reindex(columns=quality_order, fill_value=0)
sq_pct = sq.div(sq.sum(axis=1), axis=0) * 100
sq_pct_sorted = sq_pct.sort_values("Baik", ascending=False)

fig, ax = plt.subplots(figsize=(12, 5))
sq_pct_sorted.plot(kind="bar", stacked=True, ax=ax,
                   color=quality_colors, edgecolor="white", linewidth=0.5, width=0.7)
ax.set_xlabel("Stasiun"); ax.set_ylabel("Persentase Waktu (%)")
ax.set_title("Distribusi Kategori Kualitas Udara per Stasiun (Binning Clustering)",
             fontsize=12, fontweight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=9)
ax.legend(title="Kategori Udara", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.set_ylim(0, 105)
plt.tight_layout()
st.pyplot(fig); plt.close()

with st.expander("📝 Insight Analisis Lanjutan"):
    st.write("""
    - **Dingling** dan **Huairou** memiliki proporsi waktu 'Baik' tertinggi (~30%).
    - **Wanshouxigong** dan **Gucheng** memiliki proporsi 'Berbahaya' dan 'Sangat Tidak Sehat' terbesar.
    - Lebih dari **50% jam pengamatan** di semua stasiun masuk kategori 'Tidak Sehat' atau lebih buruk.
    """)

st.divider()

st.subheader("📊 Ringkasan Statistik per Stasiun")
summary = df_filter.groupby("station").agg(
    PM25_mean=("PM2.5", "mean"),
    PM25_median=("PM2.5", "median"),
    PM25_max=("PM2.5", "max"),
    PM10_mean=("PM10", "mean"),
    CO_mean=("CO", "mean"),
    Observasi=("PM2.5", "count")
).round(1).reset_index().rename(columns={"station": "Stasiun"})
st.dataframe(summary, use_container_width=True)

st.caption("Dashboard dibuat dengan Streamlit · Data: PRSA Air Quality Dataset Beijing 2013–2017")
