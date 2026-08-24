# 📈 Hisse Senedi Fiyat Tahmini - PyTorch LSTM

PyTorch ve LSTM (Long Short-Term Memory) sinir ağları kullanarak **gerçek hisse senedi verileri** ile fiyat tahmini yapan kapsamlı bir proje.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Özellikler

- ✅ **3 Farklı Kullanım Arayüzü**: Terminal, GUI, Web
- ✅ **Gerçek Veri**: yfinance API ile güncel hisse senedi verileri
- ✅ **Derin Öğrenme**: PyTorch LSTM modeli
- ✅ **Görselleştirme**: Matplotlib & Plotly ile interaktif grafikler
- ✅ **Otomatik Pipeline**: Veri toplama → İşleme → Eğitim → Tahmin
- ✅ **GPU Desteği**: Otomatik CUDA kullanımı
- ✅ **Model Kaydetme**: Eğitilmiş modelleri yeniden kullanma

## 📊 Veri Hakkında

**⚠️ ÖNEMLİ:** yfinance **geçmiş verileri** çeker (günlük kapanış fiyatları). Her çalıştırmada en güncel veriler indirilir ancak canlı/anlık (live streaming) değildir.

## 🚀 Hızlı Başlangıç

### 1️⃣ Kurulum

```bash
# Kütüphaneleri yükle
pip install -r requirements.txt
```

### 2️⃣ Kullanım Seçenekleri

#### A) Komut Satırı (En Hızlı)

```bash
# Varsayılan ayarlarla (AAPL, 50 epoch)
python main.py

# Özel ayarlarla
python main.py --ticker TSLA --epochs 100 --hidden-size 128
```

#### B) Grafiksel Arayüz (Masaüstü)

```bash
python app_gui.py
```

![GUI Ekran Görüntüsü - Modern dark theme arayüz]

**Özellikler:**
- Kolay parametre ayarlama
- Canlı eğitim logları
- Progress bar
- Tek tıkla sonuç görüntüleme

#### C) Web Arayüzü (Tarayıcı)

```bash
python -m streamlit run app_web.py
```

Tarayıcıda otomatik açılır: **http://localhost:8501**

![Web UI Ekran Görüntüsü - Streamlit modern arayüz]

**Özellikler:**
- Modern, responsive tasarım
- İnteraktif Plotly grafikleri
- Canlı metrikler
- Mobil uyumlu

## 📁 Proje Yapısı

```
├── main.py                      # Ana komut satırı uygulaması
├── app_gui.py                   # Tkinter masaüstü arayüzü
├── app_web.py                   # Streamlit web arayüzü
├── data_collection.py           # yfinance ile veri çekme
├── data_preprocessing.py        # Veri ön işleme ve ölçeklendirme
├── model.py                     # LSTM model mimarisi
├── train.py                     # Model eğitim döngüsü
├── predict.py                   # Tahmin ve görselleştirme
├── requirements.txt             # Gerekli kütüphaneler
├── KULLANIM_KILAVUZU.md        # Detaylı kullanım kılavuzu
└── README.md                    # Bu dosya
```

## 🧠 Model Mimarisi

```
Input (60 gün × 1 özellik)
    ↓
LSTM Katman 1 (hidden_size=64)
    ↓
Dropout (0.2)
    ↓
LSTM Katman 2 (hidden_size=64)
    ↓
Fully Connected (64 → 1)
    ↓
Output (1 gün tahmini)
```

- **Kayıp Fonksiyonu**: MSE (Mean Squared Error)
- **Optimizer**: Adam
- **Varsayılan Parametreler**: 50,497 parametre

## 📊 Örnek Sonuçlar

| Hisse | RMSE | MAE | MAPE | R² Score |
|-------|------|-----|------|----------|
| AAPL  | $11.96 | $9.86 | 3.45% | 0.7566 |
| TSLA  | $12.91 | $10.30 | 2.51% | 0.8916 |

## 🎯 Parametreler

| Parametre | Açıklama | Varsayılan | Değer Aralığı |
|-----------|----------|------------|---------------|
| `--ticker` | Hisse sembolü | AAPL | AAPL, TSLA, GOOGL, vb. |
| `--period` | Veri periyodu | 5y | 1y, 2y, 5y, 10y |
| `--lookback` | Geçmiş pencere | 60 | 30-120 |
| `--hidden-size` | LSTM boyutu | 64 | 32, 64, 128, 256 |
| `--num-layers` | LSTM katman | 2 | 1-3 |
| `--epochs` | Eğitim döngüsü | 50 | 10-200 |
| `--batch-size` | Batch boyutu | 32 | 16-128 |
| `--learning-rate` | Öğrenme oranı | 0.001 | 0.0001-0.01 |

## 📈 Kullanım Örnekleri

```bash
# Hızlı test (2-3 dakika)
python main.py --ticker AAPL --epochs 20

# Orta seviye (5-10 dakika)
python main.py --ticker TSLA --epochs 100 --hidden-size 128

# Güçlü model (15-20 dakika)
python main.py --ticker GOOGL --epochs 200 --hidden-size 256 --num-layers 3
```

## 📚 Detaylı Dokümantasyon

Tüm detaylar için: **[KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md)**

## 🔧 Gereksinimler

- Python 3.11+
- PyTorch 2.0+
- CUDA (opsiyonel, GPU için)
- 4GB+ RAM
- İnternet bağlantısı (veri indirme için)

## 📝 Lisans

MIT License - Özgürce kullanabilir, değiştirebilir ve paylaşabilirsiniz.

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## ⚠️ Uyarı

Bu proje **sadece eğitim amaçlıdır**. Gerçek yatırım kararları için kullanmayın. Finansal piyasalar tahmin edilemez ve geçmiş performans gelecek performansı garanti etmez.
