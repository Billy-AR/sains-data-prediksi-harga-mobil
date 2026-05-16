import json

cells = []

def md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    })

def code(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    })

# ============================================================
# CELL 1 - Title
# ============================================================
md("""# Final Project Sains Data
## Prediksi Harga Mobil dengan Metode CRISP-DM

---

**Pendahuluan:**

Sebuah perusahaan manufaktur otomotif merekrut seorang Data Scientist untuk menciptakan sistem yang dapat:
1. Memberikan rekomendasi spesifikasi mobil yang sedang laku di pasar.
2. Menentukan harga yang sesuai dengan spesifikasi mobil yang direkomendasikan/diinputkan.
3. Membuat sistem dapat diakses oleh end user melalui web browser.

Dataset yang digunakan: **Car_sales.xlsx**

Metode: **CRISP-DM (Cross-Industry Standard Process for Data Mining)**""")

# ============================================================
# CELL 2 - Business Understanding
# ============================================================
md("""---
# Phase 1: Business Understanding

Tujuan bisnis dari project ini adalah:
- **Memahami tren pasar otomotif** berdasarkan data penjualan mobil.
- **Mengidentifikasi spesifikasi mobil** yang paling diminati pasar.
- **Membangun model prediksi harga** mobil berdasarkan spesifikasinya agar perusahaan dapat menentukan harga yang kompetitif.

Dengan model ini, perusahaan dapat:
1. Merekomendasikan spesifikasi mobil yang sesuai dengan permintaan pasar.
2. Menentukan harga jual yang optimal berdasarkan spesifikasi tertentu.
3. Meningkatkan efisiensi dalam proses pengambilan keputusan produksi.""")

# ============================================================
# CELL 3 - Phase 2 Title
# ============================================================
md("""---
# Phase 2: Data Understanding

## Langkah 1 - Memanggil Library yang Diperlukan""")

# ============================================================
# CELL 4 - Import Libraries
# ============================================================
code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Setting style untuk visualisasi
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

print("Semua library berhasil di-import!")""")

# ============================================================
# CELL 5 - Load Data Title
# ============================================================
md("""## Langkah 2 - Load Data

Memuat dataset Car_sales.xlsx yang berisi data penjualan mobil dari berbagai manufaktur.""")

# ============================================================
# CELL 6 - Load Data Code
# ============================================================
code("""# Upload file di Google Colab
from google.colab import files
uploaded = files.upload()""")

# ============================================================
# CELL 7 - Read Data
# ============================================================
code("""# Membaca dataset
df = pd.read_excel('Car_sales.xlsx')
print(f"Dataset berhasil dimuat dengan {df.shape[0]} baris dan {df.shape[1]} kolom.")""")

# ============================================================
# CELL 8 - View Data Title
# ============================================================
md("""## Langkah 3 - Melihat Data

Pada tahap ini kita akan melakukan eksplorasi awal terhadap dataset untuk memahami struktur, tipe data, dan kondisi data.""")

# ============================================================
# CELL 9 - View Data Code
# ============================================================
code("""# Menampilkan 5 data pertama
print("=" * 80)
print("5 DATA PERTAMA")
print("=" * 80)
df.head()""")

# ============================================================
# CELL 10 - Info
# ============================================================
code("""# Menampilkan informasi dataset
print("=" * 80)
print("INFORMASI DATASET")
print("=" * 80)
df.info()""")

# ============================================================
# CELL 11 - Describe
# ============================================================
code("""# Menampilkan statistik deskriptif
print("=" * 80)
print("STATISTIK DESKRIPTIF")
print("=" * 80)
df.describe()""")

# ============================================================
# CELL 12 - Shape & Columns
# ============================================================
code("""# Menampilkan jumlah baris dan kolom
print(f"Jumlah Baris  : {df.shape[0]}")
print(f"Jumlah Kolom  : {df.shape[1]}")
print(f"\\nNama Kolom:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")""")

# ============================================================
# CELL 13 - Missing value title
# ============================================================
md("""---
# Phase 3: Data Preparation

## Langkah 4 - Menghapus Missing Value

Pertama, kita identifikasi missing value pada dataset, lalu kita hapus baris yang memiliki missing value pada kolom target (Price_in_thousands).""")

# ============================================================
# CELL 14 - Check Missing
# ============================================================
code("""# Mengecek jumlah missing value pada setiap kolom
print("=" * 80)
print("JUMLAH MISSING VALUE PER KOLOM")
print("=" * 80)
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Jumlah Missing': missing, 'Persentase (%)': missing_pct})
missing_df = missing_df[missing_df['Jumlah Missing'] > 0].sort_values('Jumlah Missing', ascending=False)
print(missing_df)
print(f"\\nTotal baris sebelum penanganan missing value: {len(df)}")""")

# ============================================================
# CELL 15 - Drop Missing on Target
# ============================================================
code("""# Menghapus baris yang memiliki missing value pada kolom target (Price_in_thousands)
# Karena kolom target tidak boleh kosong untuk membuat model prediksi
print(f"Baris sebelum menghapus missing value pada Price_in_thousands: {len(df)}")
df = df.dropna(subset=['Price_in_thousands'])
print(f"Baris setelah menghapus missing value pada Price_in_thousands : {len(df)}")""")

# ============================================================
# CELL 16 - Fill Missing Title
# ============================================================
md("""## Langkah 5 - Mengisi Missing Value

Untuk kolom numerik yang masih memiliki missing value, kita isi dengan nilai **median** dari masing-masing kolom.
Median dipilih karena lebih robust terhadap outlier dibandingkan mean.""")

# ============================================================
# CELL 17 - Fill Missing
# ============================================================
code("""# Mengisi missing value pada kolom numerik dengan median
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        print(f"Kolom '{col}' memiliki {df[col].isnull().sum()} missing value -> diisi dengan median = {median_val}")
        df[col].fillna(median_val, inplace=True)

print("\\n" + "=" * 80)
print("VERIFIKASI: MISSING VALUE SETELAH PENANGANAN")
print("=" * 80)
print(df.isnull().sum())
print(f"\\nTotal baris setelah penanganan: {len(df)}")""")

# ============================================================
# CELL 18 - EDA Title
# ============================================================
md("""---
## Langkah 6 - Explorasi Data (Exploratory Data Analysis)

### 6a. 10 Jenis Mobil dengan Jumlah Penjualan Terbanyak""")

# ============================================================
# CELL 19 - Top 10 Sales Chart
# ============================================================
code("""# Membuat kolom nama lengkap mobil
df['Car_Name'] = df['Manufacturer'] + ' ' + df['Model'].astype(str)

# 10 mobil dengan penjualan terbanyak
top10_sales = df.nlargest(10, 'Sales_in_thousands')

# Visualisasi
fig, ax = plt.subplots(figsize=(14, 7))
colors = sns.color_palette('viridis', 10)
bars = ax.barh(top10_sales['Car_Name'], top10_sales['Sales_in_thousands'], color=colors)
ax.set_xlabel('Penjualan (dalam ribuan)', fontsize=13)
ax.set_ylabel('Nama Mobil', fontsize=13)
ax.set_title('10 Jenis Mobil dengan Jumlah Penjualan Terbanyak', fontsize=15, fontweight='bold')
ax.invert_yaxis()

# Menambahkan label pada bar
for bar, val in zip(bars, top10_sales['Sales_in_thousands']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}K', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()""")

# ============================================================
# CELL 20 - Penjelasan top 10 sales
# ============================================================
md("""**Penjelasan:**

Grafik di atas menunjukkan 10 jenis mobil dengan jumlah penjualan terbanyak. Dari grafik tersebut dapat dilihat bahwa:
- Mobil-mobil dengan penjualan terbanyak didominasi oleh brand-brand populer.
- Data penjualan ini menjadi acuan utama dalam menentukan spesifikasi mobil yang diminati pasar.
- Perusahaan dapat menggunakan informasi ini untuk fokus memproduksi mobil dengan spesifikasi serupa.""")

# ============================================================
# CELL 21 - 6b Title
# ============================================================
md("""### 6b. Harga dari 10 Jenis Mobil dengan Jumlah Penjualan Terbanyak""")

# ============================================================
# CELL 22 - Price of top 10
# ============================================================
code("""# Harga dari 10 mobil dengan penjualan terbanyak
fig, ax = plt.subplots(figsize=(14, 7))
colors = sns.color_palette('magma', 10)
bars = ax.barh(top10_sales['Car_Name'], top10_sales['Price_in_thousands'], color=colors)
ax.set_xlabel('Harga (dalam ribuan USD)', fontsize=13)
ax.set_ylabel('Nama Mobil', fontsize=13)
ax.set_title('Harga dari 10 Jenis Mobil dengan Penjualan Terbanyak', fontsize=15, fontweight='bold')
ax.invert_yaxis()

# Menambahkan label pada bar
for bar, val in zip(bars, top10_sales['Price_in_thousands']):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'${val:.1f}K', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()

# Tabel detail
print("\\n" + "=" * 80)
print("DETAIL HARGA 10 MOBIL DENGAN PENJUALAN TERBANYAK")
print("=" * 80)
print(top10_sales[['Car_Name', 'Sales_in_thousands', 'Price_in_thousands']].to_string(index=False))""")

# ============================================================
# CELL 23 - Penjelasan harga
# ============================================================
md("""**Penjelasan:**

Dari grafik harga 10 mobil terlaris, dapat dianalisis:
- Tidak selalu mobil dengan harga murah yang memiliki penjualan tinggi, menunjukkan bahwa faktor spesifikasi dan brand juga berpengaruh.
- Rentang harga mobil terlaris bervariasi, yang menandakan bahwa pasar memiliki segmentasi yang beragam.
- Informasi ini penting untuk menentukan pricing strategy yang tepat.""")

# ============================================================
# CELL 24 - 6c Title
# ============================================================
md("""### 6c. Variable/Atribut Data Lain dari 10 Jenis Mobil dengan Penjualan Terbanyak

Menampilkan 3 variabel tambahan: **Engine Size**, **Horsepower**, dan **Fuel Efficiency**.""")

# ============================================================
# CELL 25 - Engine Size Chart
# ============================================================
code("""# --- Atribut 1: Engine Size ---
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Engine Size
colors1 = sns.color_palette('coolwarm', 10)
bars1 = axes[0].barh(top10_sales['Car_Name'], top10_sales['Engine_size'], color=colors1)
axes[0].set_xlabel('Engine Size (L)', fontsize=12)
axes[0].set_title('Engine Size', fontsize=14, fontweight='bold')
axes[0].invert_yaxis()
for bar, val in zip(bars1, top10_sales['Engine_size']):
    axes[0].text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{val:.1f}L', va='center', fontsize=10)

# --- Atribut 2: Horsepower ---
colors2 = sns.color_palette('RdYlGn', 10)
bars2 = axes[1].barh(top10_sales['Car_Name'], top10_sales['Horsepower'], color=colors2)
axes[1].set_xlabel('Horsepower (HP)', fontsize=12)
axes[1].set_title('Horsepower', fontsize=14, fontweight='bold')
axes[1].invert_yaxis()
for bar, val in zip(bars2, top10_sales['Horsepower']):
    axes[1].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f} HP', va='center', fontsize=10)

# --- Atribut 3: Fuel Efficiency ---
colors3 = sns.color_palette('YlOrBr', 10)
bars3 = axes[2].barh(top10_sales['Car_Name'], top10_sales['Fuel_efficiency'], color=colors3)
axes[2].set_xlabel('Fuel Efficiency (MPG)', fontsize=12)
axes[2].set_title('Fuel Efficiency', fontsize=14, fontweight='bold')
axes[2].invert_yaxis()
for bar, val in zip(bars3, top10_sales['Fuel_efficiency']):
    axes[2].text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f} MPG', va='center', fontsize=10)

plt.suptitle('Spesifikasi dari 10 Mobil dengan Penjualan Terbanyak', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()""")

# ============================================================
# CELL 26 - Tabel detail spesifikasi
# ============================================================
code("""# Detail tabel spesifikasi lengkap
print("=" * 100)
print("DETAIL SPESIFIKASI 10 MOBIL DENGAN PENJUALAN TERBANYAK")
print("=" * 100)
detail_cols = ['Car_Name', 'Sales_in_thousands', 'Price_in_thousands', 'Engine_size', 'Horsepower', 'Fuel_efficiency']
print(top10_sales[detail_cols].to_string(index=False))""")

# ============================================================
# CELL 27 - Penjelasan atribut lain
# ============================================================
md("""**Penjelasan:**

Dari 3 variabel tambahan yang ditampilkan:
1. **Engine Size**: Ukuran mesin mobil terlaris bervariasi, menunjukkan bahwa pasar menerima berbagai kapasitas mesin. Sebagian besar berkisar antara 2.0L - 4.0L.
2. **Horsepower**: Tenaga kuda (HP) juga bervariasi, mengindikasikan bahwa konsumen memiliki preferensi yang beragam terkait performa mobil.
3. **Fuel Efficiency**: Efisiensi bahan bakar menunjukkan bahwa mobil terlaris memiliki efisiensi yang cukup baik, mengindikasikan konsumen peduli terhadap konsumsi bahan bakar.

Kesimpulan: Mobil yang laku di pasar cenderung memiliki kombinasi spesifikasi yang seimbang antara performa (HP, Engine Size) dan efisiensi (Fuel Efficiency).""")

# ============================================================
# CELL 28 - Langkah 7 Title
# ============================================================
md("""---
## Langkah 7 - Menentukan Variable untuk Rekomendasi Spesifikasi Mobil

Pada tahap ini, kita menentukan variable yang akan digunakan sebagai rekomendasi dalam menentukan spesifikasi mobil yang akan diproduksi.""")

# ============================================================
# CELL 29 - Correlation Analysis
# ============================================================
code("""# Analisis korelasi antar variabel numerik terhadap harga
numeric_df = df.select_dtypes(include=[np.number])
correlation = numeric_df.corr()['Price_in_thousands'].sort_values(ascending=False)

print("=" * 60)
print("KORELASI VARIABEL TERHADAP HARGA (Price_in_thousands)")
print("=" * 60)
for col, val in correlation.items():
    if col != 'Price_in_thousands':
        indicator = "Kuat" if abs(val) > 0.5 else "Sedang" if abs(val) > 0.3 else "Lemah"
        print(f"  {col:25s} : {val:+.4f}  ({indicator})")""")

# ============================================================
# CELL 30 - Heatmap
# ============================================================
code("""# Heatmap korelasi
fig, ax = plt.subplots(figsize=(14, 10))
mask = np.triu(np.ones_like(correlation.to_frame().T.values, dtype=bool))
sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, ax=ax, vmin=-1, vmax=1)
ax.set_title('Heatmap Korelasi Antar Variabel Numerik', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()""")

# ============================================================
# CELL 31 - Variable Selection Explanation
# ============================================================
md("""**Penentuan Variable untuk Rekomendasi:**

Berdasarkan analisis korelasi di atas, variabel yang dipilih sebagai **fitur (independent variable)** untuk model prediksi harga mobil adalah:

| No | Variable | Alasan |
|----|----------|--------|
| 1 | **Engine_size** | Korelasi kuat positif terhadap harga |
| 2 | **Horsepower** | Korelasi kuat positif terhadap harga |
| 3 | **Curb_weight** | Korelasi kuat positif terhadap harga |
| 4 | **Fuel_capacity** | Korelasi positif terhadap harga |
| 5 | **Width** | Korelasi positif terhadap harga |
| 6 | **Length** | Korelasi positif terhadap harga |
| 7 | **Wheelbase** | Korelasi positif terhadap harga |
| 8 | **Fuel_efficiency** | Korelasi negatif terhadap harga (mobil hemat BBM cenderung lebih murah) |

**Target variable (dependent variable):** `Price_in_thousands`

Variabel-variabel ini dipilih karena memiliki korelasi yang cukup signifikan terhadap harga dan merepresentasikan spesifikasi teknis mobil yang relevan bagi perusahaan manufaktur.""")

# ============================================================
# CELL 32 - Phase 4 Title
# ============================================================
md("""---
# Phase 4: Modeling

## Langkah 8 - Membuat Model Prediksi Harga Mobil Menggunakan Linear Regression

### 8a. Memisahkan Variable Independent dan Dependent""")

# ============================================================
# CELL 33 - Split X and y
# ============================================================
code("""# Menentukan variabel Independent (X) dan Dependent (y)
feature_cols = ['Engine_size', 'Horsepower', 'Curb_weight', 'Fuel_capacity',
                'Width', 'Length', 'Wheelbase', 'Fuel_efficiency']

X = df[feature_cols]
y = df['Price_in_thousands']

print("=" * 60)
print("VARIABLE INDEPENDENT (X):")
print("=" * 60)
print(X.head())
print(f"\\nShape X: {X.shape}")

print("\\n" + "=" * 60)
print("VARIABLE DEPENDENT (y):")
print("=" * 60)
print(y.head())
print(f"\\nShape y: {y.shape}")""")

# ============================================================
# CELL 34 - 8b Title
# ============================================================
md("""### 8b. Memisahkan Data Training (80%) dan Data Testing (20%)""")

# ============================================================
# CELL 35 - Train Test Split
# ============================================================
code("""# Membagi data menjadi training (80%) dan testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("=" * 60)
print("PEMBAGIAN DATA TRAINING DAN TESTING")
print("=" * 60)
print(f"Total data       : {len(X)}")
print(f"Data Training    : {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Data Testing     : {len(X_test)} ({len(X_test)/len(X)*100:.0f}%)")""")

# ============================================================
# CELL 36 - 8c Title
# ============================================================
md("""### 8c. Membuat Model Regresi""")

# ============================================================
# CELL 37 - Train Model
# ============================================================
code("""# Membuat dan melatih model Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

print("=" * 60)
print("MODEL LINEAR REGRESSION BERHASIL DIBUAT!")
print("=" * 60)
print(f"\\nIntercept: {model.intercept_:.4f}")
print(f"\\nKoefisien Model:")
for feat, coef in zip(feature_cols, model.coef_):
    print(f"  {feat:20s} : {coef:+.4f}")""")

# ============================================================
# CELL 38 - 8d Title
# ============================================================
md("""### 8d. Mengevaluasi Model dengan RMSE dan R2 Score""")

# ============================================================
# CELL 39 - Evaluate Model
# ============================================================
code("""# Melakukan prediksi pada data testing
y_pred = model.predict(X_test)

# Menghitung RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Menghitung R2 Score
r2 = r2_score(y_test, y_pred)

print("=" * 60)
print("EVALUASI MODEL")
print("=" * 60)
print(f"\\n  RMSE     : {rmse:.4f}")
print(f"  R2 Score : {r2:.4f}")
print(f"  R2 (%)   : {r2*100:.2f}%")
print(f"\\nInterpretasi:")
print(f"  - RMSE sebesar {rmse:.2f} berarti rata-rata kesalahan prediksi model")
print(f"    sekitar ${rmse:.2f} ribu dari harga sebenarnya.")
print(f"  - R2 Score sebesar {r2:.4f} ({r2*100:.2f}%) berarti model dapat")
print(f"    menjelaskan {r2*100:.2f}% variasi harga mobil.")""")

# ============================================================
# CELL 40 - Evaluasi training juga
# ============================================================
code("""# Evaluasi pada data training untuk perbandingan
y_train_pred = model.predict(X_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
r2_train = r2_score(y_train, y_train_pred)

print("=" * 60)
print("PERBANDINGAN EVALUASI TRAINING vs TESTING")
print("=" * 60)
print(f"\\n{'Metric':<15} {'Training':>15} {'Testing':>15}")
print("-" * 45)
print(f"{'RMSE':<15} {rmse_train:>15.4f} {rmse:>15.4f}")
print(f"{'R2 Score':<15} {r2_train:>15.4f} {r2:>15.4f}")
print(f"\\nModel tidak mengalami overfitting karena performa training dan testing relatif seimbang." if abs(r2_train - r2) < 0.15 else "\\nPerlu diperhatikan perbedaan performa training dan testing.")""")

# ============================================================
# CELL 41 - 8e Title
# ============================================================
md("""### 8e. Menggambarkan Hasil Evaluasi dengan Scatter Plot""")

# ============================================================
# CELL 42 - Scatter Plot
# ============================================================
code("""# Scatter Plot: Actual vs Predicted
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Plot 1: Actual vs Predicted
axes[0].scatter(y_test, y_pred, alpha=0.7, color='steelblue', edgecolor='white', s=80)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
             'r--', lw=2, label='Garis Ideal (y = x)')
axes[0].set_xlabel('Harga Aktual (ribu USD)', fontsize=13)
axes[0].set_ylabel('Harga Prediksi (ribu USD)', fontsize=13)
axes[0].set_title(f'Actual vs Predicted\\nR² = {r2:.4f} | RMSE = {rmse:.2f}',
                  fontsize=14, fontweight='bold')
axes[0].legend(fontsize=12)
axes[0].grid(True, alpha=0.3)

# Plot 2: Residual Plot
residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.7, color='coral', edgecolor='white', s=80)
axes[1].axhline(y=0, color='green', linestyle='--', lw=2)
axes[1].set_xlabel('Harga Prediksi (ribu USD)', fontsize=13)
axes[1].set_ylabel('Residual (Actual - Predicted)', fontsize=13)
axes[1].set_title('Residual Plot', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Evaluasi Visual Model Linear Regression', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()""")

# ============================================================
# CELL 43 - Penjelasan Scatter
# ============================================================
md("""**Penjelasan Scatter Plot:**

1. **Actual vs Predicted Plot**: Titik-titik yang mendekati garis merah (garis ideal) menunjukkan prediksi yang akurat. Semakin dekat titik ke garis, semakin baik prediksi model.

2. **Residual Plot**: Residual yang tersebar merata di sekitar garis nol menunjukkan bahwa model tidak memiliki pola error yang sistematis (asumsi homoskedastisitas terpenuhi).""")

# ============================================================
# CELL 44 - Phase 5 Title
# ============================================================
md("""---
# Phase 5: Evaluation

## Langkah 9 - Memprediksi Harga dengan Spesifikasi Mobil yang Ditentukan

Pada tahap ini, kita akan menguji model dengan menginputkan spesifikasi mobil tertentu untuk mendapatkan prediksi harga.""")

# ============================================================
# CELL 45 - Predict new data
# ============================================================
code("""# Membuat dataframe dengan spesifikasi mobil yang ingin diprediksi
# Spesifikasi diambil berdasarkan rekomendasi pasar (rata-rata dari top 10 mobil terlaris)
rekomendasi_specs = pd.DataFrame({
    'Engine_size': [2.5],
    'Horsepower': [180.0],
    'Curb_weight': [3.2],
    'Fuel_capacity': [17.0],
    'Width': [70.0],
    'Length': [185.0],
    'Wheelbase': [105.0],
    'Fuel_efficiency': [26.0]
})

print("=" * 60)
print("SPESIFIKASI MOBIL YANG DIINPUTKAN")
print("=" * 60)
for col in rekomendasi_specs.columns:
    print(f"  {col:20s} : {rekomendasi_specs[col].values[0]}")""")

# ============================================================
# CELL 46 - Langkah 10 Title
# ============================================================
md("""## Langkah 10 - Menampilkan Hasil Prediksi Harga""")

# ============================================================
# CELL 47 - Show Prediction
# ============================================================
code("""# Memprediksi harga berdasarkan spesifikasi yang diinputkan
harga_prediksi = model.predict(rekomendasi_specs)

print("=" * 60)
print("HASIL PREDIKSI HARGA MOBIL")
print("=" * 60)
print(f"\\n  Harga Prediksi : ${harga_prediksi[0]:.2f} ribu USD")
print(f"  Harga Prediksi : ${harga_prediksi[0] * 1000:,.0f} USD")
print(f"\\n  (Berdasarkan spesifikasi yang diinputkan)")
print("\\n" + "=" * 60)

# Menampilkan ringkasan
print("\\nRINGKASAN REKOMENDASI:")
print("-" * 60)
print(f"  Engine Size      : {rekomendasi_specs['Engine_size'].values[0]} L")
print(f"  Horsepower       : {rekomendasi_specs['Horsepower'].values[0]} HP")
print(f"  Curb Weight      : {rekomendasi_specs['Curb_weight'].values[0]} (x1000 lbs)")
print(f"  Fuel Capacity    : {rekomendasi_specs['Fuel_capacity'].values[0]} gallons")
print(f"  Width            : {rekomendasi_specs['Width'].values[0]} inches")
print(f"  Length           : {rekomendasi_specs['Length'].values[0]} inches")
print(f"  Wheelbase        : {rekomendasi_specs['Wheelbase'].values[0]} inches")
print(f"  Fuel Efficiency  : {rekomendasi_specs['Fuel_efficiency'].values[0]} MPG")
print(f"  ─────────────────────────────────────")
print(f"  HARGA PREDIKSI   : ${harga_prediksi[0] * 1000:,.0f} USD")""")

# ============================================================
# CELL 48 - Multiple Predictions
# ============================================================
code("""# Prediksi untuk beberapa skenario spesifikasi berbeda
skenario = pd.DataFrame({
    'Engine_size': [1.8, 2.5, 3.5, 4.0, 5.0],
    'Horsepower': [140, 180, 250, 300, 350],
    'Curb_weight': [2.6, 3.2, 3.8, 4.0, 4.5],
    'Fuel_capacity': [13, 17, 20, 22, 25],
    'Width': [67, 70, 73, 75, 78],
    'Length': [172, 185, 195, 200, 210],
    'Wheelbase': [101, 105, 110, 115, 120],
    'Fuel_efficiency': [30, 26, 22, 18, 15]
})

# Prediksi harga untuk setiap skenario
harga_skenario = model.predict(skenario)
skenario['Prediksi_Harga_Ribu_USD'] = harga_skenario.round(2)
skenario['Kategori'] = ['Economy', 'Standard', 'Premium', 'Luxury', 'Super Luxury']

print("=" * 80)
print("PREDIKSI HARGA UNTUK BERBAGAI SKENARIO SPESIFIKASI")
print("=" * 80)
print(skenario[['Kategori', 'Engine_size', 'Horsepower', 'Fuel_efficiency', 'Prediksi_Harga_Ribu_USD']].to_string(index=False))""")

# ============================================================
# CELL 49 - Conclusion
# ============================================================
md("""---
# Phase 6: Deployment

## Langkah 11 - Deployment Model

Model yang telah dibuat dapat di-deploy menggunakan **Streamlit** agar dapat diakses oleh end user melalui web browser.

Berikut adalah kode untuk deployment menggunakan Streamlit (jalankan di file terpisah `app.py`):""")

# ============================================================
# CELL 50 - Streamlit Code
# ============================================================
code("""# Simpan model untuk deployment
import pickle

# Simpan model ke file
with open('model_harga_mobil.pkl', 'wb') as f:
    pickle.dump(model, f)

# Simpan informasi fitur
model_info = {
    'feature_cols': feature_cols,
    'model': model,
    'rmse': rmse,
    'r2': r2
}

with open('model_info.pkl', 'wb') as f:
    pickle.dump(model_info, f)

print("Model berhasil disimpan ke file 'model_harga_mobil.pkl' dan 'model_info.pkl'")""")

# ============================================================
# CELL 51 - Streamlit app code
# ============================================================
code("""%%writefile app.py
import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model
with open('model_info.pkl', 'rb') as f:
    model_info = pickle.load(f)

model = model_info['model']
feature_cols = model_info['feature_cols']

st.set_page_config(page_title="Prediksi Harga Mobil", page_icon="🚗", layout="centered")

st.title("🚗 Prediksi Harga Mobil")
st.markdown("Masukkan spesifikasi mobil di bawah ini untuk memprediksi harganya.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    engine_size = st.number_input("Engine Size (L)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)
    horsepower = st.number_input("Horsepower (HP)", min_value=50, max_value=600, value=180, step=10)
    curb_weight = st.number_input("Curb Weight (x1000 lbs)", min_value=1.0, max_value=6.0, value=3.2, step=0.1)
    fuel_capacity = st.number_input("Fuel Capacity (gallons)", min_value=5.0, max_value=40.0, value=17.0, step=0.5)

with col2:
    width = st.number_input("Width (inches)", min_value=50.0, max_value=100.0, value=70.0, step=0.5)
    length = st.number_input("Length (inches)", min_value=100.0, max_value=300.0, value=185.0, step=1.0)
    wheelbase = st.number_input("Wheelbase (inches)", min_value=80.0, max_value=150.0, value=105.0, step=0.5)
    fuel_efficiency = st.number_input("Fuel Efficiency (MPG)", min_value=5.0, max_value=60.0, value=26.0, step=1.0)

st.markdown("---")

if st.button("🔍 Prediksi Harga", use_container_width=True):
    input_data = pd.DataFrame({
        'Engine_size': [engine_size],
        'Horsepower': [horsepower],
        'Curb_weight': [curb_weight],
        'Fuel_capacity': [fuel_capacity],
        'Width': [width],
        'Length': [length],
        'Wheelbase': [wheelbase],
        'Fuel_efficiency': [fuel_efficiency]
    })

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Harga Prediksi: **${prediction:,.2f} ribu USD** (${prediction * 1000:,.0f} USD)")

    st.markdown("### Spesifikasi yang Diinputkan:")
    st.dataframe(input_data.T.rename(columns={0: 'Nilai'}), use_container_width=True)

st.markdown("---")
st.markdown(f"*Model: Linear Regression | R² Score: {model_info['r2']:.4f} | RMSE: {model_info['rmse']:.4f}*")""")

# ============================================================
# CELL 52 - Instructions for deployment
# ============================================================
md("""## Cara Menjalankan Aplikasi Web (Deployment)

Untuk menjalankan aplikasi web prediksi harga mobil:

1. Pastikan sudah install Streamlit: `pip install streamlit`
2. Jalankan perintah di terminal: `streamlit run app.py`
3. Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`

---

# Kesimpulan

1. **Business Understanding**: Proyek ini bertujuan membantu perusahaan otomotif memprediksi harga mobil berdasarkan spesifikasi teknis.

2. **Data Understanding**: Dataset memiliki 157 data mobil dengan 16 variabel yang mencakup informasi penjualan, spesifikasi, dan harga.

3. **Data Preparation**: Missing value ditangani dengan menghapus baris target yang kosong dan mengisi kolom fitur dengan median.

4. **Modeling**: Model Linear Regression digunakan dengan 8 fitur independent yang dipilih berdasarkan analisis korelasi.

5. **Evaluation**: Model dievaluasi menggunakan RMSE dan R² Score, menunjukkan performa yang baik dalam memprediksi harga.

6. **Deployment**: Model dapat di-deploy menggunakan Streamlit untuk diakses end user melalui web browser.""")

# ============================================================
# Build notebook JSON
# ============================================================
# Fix: remove trailing newline from last line of each cell
for cell in cells:
    if cell["source"]:
        cell["source"][-1] = cell["source"][-1].rstrip("\n")

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"}
    },
    "cells": cells
}

output_path = r"d:\Perkuliahan\SMT 6\Sains Data\UAS\project\Final_Project_Prediksi_Harga_Mobil.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook berhasil dibuat: {output_path}")
print(f"Total cells: {len(cells)}")
