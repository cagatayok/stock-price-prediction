# 🧪 Nasıl Test Edilir?

## ✅ Şu Anda Çalışan Arayüzler

### 1️⃣ Tkinter GUI (Masaüstü)
- ✅ **Durum**: ÇALIŞIYOR
- 📍 **Konum**: Masaüstünüzde pencere açık olmalı
- 🎯 **Ne Yapmalı**: 
  - Sol panelden parametreleri ayarlayın
  - "🚀 Eğitimi Başlat" butonuna tıklayın
  - Sağ panelde logları izleyin

### 2️⃣ Streamlit Web (Tarayıcı)
- ✅ **Durum**: ÇALIŞIYOR
- 🌐 **URL**: http://localhost:8501
- 🎯 **Ne Yapmalı**:
  - Tarayıcınızı açın
  - `http://localhost:8501` adresine gidin
  - Modern web arayüzü görünecek
  - Sol menüden ayarlar, ortada sonuçlar

---

## 🎮 Test Senaryoları

### ⚡ 1. Hızlı Test (2-3 dakika)

**Terminal:**
```bash
python main.py --ticker AAPL --epochs 20 --batch-size 64
```

**GUI veya Web:**
- Hisse: AAPL
- Epoch: 20
- Batch Size: 64
- Diğerleri varsayılan

**Beklenen Sonuç:**
- 2-3 dakikada bitecek
- RMSE ~$12-15 civarı
- Grafikler oluşacak

---

### 🚀 2. Orta Seviye Test (5-7 dakika)

**Terminal:**
```bash
python main.py --ticker TSLA --epochs 50 --hidden-size 128
```

**GUI veya Web:**
- Hisse: TSLA
- Epoch: 50
- Hidden Size: 128
- Num Layers: 2

**Beklenen Sonuç:**
- 5-7 dakikada bitecek
- RMSE ~$10-13 civarı
- R² Score ~0.85-0.90
- MAPE %2-3 arası (çok iyi!)

---

### 🏆 3. Farklı Hisseler (Karşılaştırma)

**Test 1 - Apple (Düşük Volatilite):**
```bash
python main.py --ticker AAPL --epochs 50
```
Beklenti: İyi sonuçlar (MAPE %3-5)

**Test 2 - Tesla (Yüksek Volatilite):**
```bash
python main.py --ticker TSLA --epochs 50
```
Beklenti: Zorlayıcı ama iyi (MAPE %2-4)

**Test 3 - Microsoft (Dengeli):**
```bash
python main.py --ticker MSFT --epochs 50
```
Beklenti: Çok iyi sonuçlar (MAPE %2-3)

**Test 4 - Nvidia (Teknoloji):**
```bash
python main.py --ticker NVDA --epochs 50
```
Beklenti: İyi sonuçlar (MAPE %3-5)

---

## 📊 Sonuçları Kontrol Etme

### 1. Grafikleri Açma

**Terminal'den otomatik:**
Eğitim bitince grafikler Desktop klasörünüzde:
- `{TICKER}_predictions.png` - Tahmin grafiği
- `{TICKER}_training_history.png` - Eğitim grafiği
- `{TICKER}_predictions_zoomed.png` - Detaylı görünüm

**GUI'den:**
- "📊 Sonuçları Aç" butonuna tıklayın
- Tüm grafikler otomatik açılır

**Web'den:**
- Zaten sayfa içinde gösterilir
- İnteraktif grafiklerde zoom yapabilirsiniz

---

### 2. Metrikleri Yorumlama

**✅ ÇOK İYİ SONUÇ:**
- MAPE: %1-3
- R² Score: 0.85-0.95
- Grafik: Çizgiler çok yakın

**✅ İYİ SONUÇ:**
- MAPE: %3-5
- R² Score: 0.75-0.85
- Grafik: Çizgiler benzer trend

**⚠️ ORTA SONUÇ:**
- MAPE: %5-10
- R² Score: 0.60-0.75
- Grafik: Bazı sapmalar var

**❌ ZAYIF SONUÇ:**
- MAPE: %10+
- R² Score: <0.60
- Grafik: Büyük farklar

---

## 🎯 GUI Test Adımları (Detaylı)

### Adım 1: Pencereyi Kontrol Edin
- Masaüstünüzde dark theme'li bir pencere açık olmalı
- Başlık: "📈 Hisse Senedi Fiyat Tahmini"

### Adım 2: Parametreleri Ayarlayın
Sol panelde:
1. Hisse Sembolü: `AAPL` yazın
2. Veri Periyodu: `5y` seçin
3. Geçmiş Pencere: `60` bırakın
4. LSTM Boyutu: `64` seçin
5. Epoch Sayısı: `30` yazın (hızlı test için)

### Adım 3: Eğitimi Başlatın
- Yeşil "🚀 Eğitimi Başlat" butonuna tıklayın
- Progress bar başlayacak
- Sağ tarafta loglar akacak

### Adım 4: İzleyin
```
[12:30:45] 🚀 EĞİTİM BAŞLIYOR
[12:30:46] 📥 Veri indiriliyor...
[12:30:50] ✅ 1255 veri noktası indirildi
[12:30:51] 🔄 Veri işleniyor...
[12:30:52] ✅ Veri hazırlandı
[12:30:53] 🧠 Model oluşturuluyor...
...
```

### Adım 5: Sonuçları Görün
- Eğitim bitince durum "✅ Hazır" olacak
- "📊 Sonuçları Aç" butonuna tıklayın
- Grafikler otomatik açılır

---

## 🌐 Web Test Adımları (Detaylı)

### Adım 1: Tarayıcıyı Açın
- Chrome, Firefox, Edge veya Safari
- Adres: `http://localhost:8501`

### Adım 2: Arayüzü Görün
- Modern, koyu temalı sayfa
- Sol tarafta sidebar (ayarlar)
- Ortada ana içerik

### Adım 3: Popüler Hisse Butonları
Ana sayfada 4 buton:
- 🍎 Apple (AAPL)
- ⚡ Tesla (TSLA)
- 🔍 Google (GOOGL)
- 🪟 Microsoft (MSFT)

Birine tıklayın → otomatik seçilir

### Adım 4: Parametreler
Sol sidebar'dan:
1. Hisse sembolü (zaten seçili)
2. Epoch: 30 yapın (slider ile)
3. "🚀 Eğitimi Başlat"

### Adım 5: Canlı Sonuçlar
- Progress bar ilerleyecek
- Metrikler güncellenecek
- Grafikler oluşacak
- İnteraktif zoom yapabilirsiniz

---

## 🔍 Sorun mu Var?

### GUI Açılmadı
```bash
# Tekrar çalıştırın
python app_gui.py
```

### Web Açılmadı
```bash
# Process'i durdur, yeniden başlat
Ctrl+C (terminal'de)
python -m streamlit run app_web.py
```

### "No module" Hatası
```bash
# Kütüphaneleri tekrar yükle
python -m pip install -r requirements.txt
```

### Yavaş Çalışıyor
- Epoch sayısını azaltın (50 → 20)
- Batch size'ı artırın (32 → 64)

---

## 📋 Checklist

Test yaparken kontrol edin:

- [ ] GUI penceresi açıldı mı?
- [ ] Web arayüzü http://localhost:8501 açılıyor mu?
- [ ] Terminal'den komut çalışıyor mu?
- [ ] Veri indiriliyor mu?
- [ ] Eğitim başlıyor mu?
- [ ] Loglar akıyor mu?
- [ ] Grafikler oluşuyor mu?
- [ ] Metrikler mantıklı mı?

---

## 🎓 Önerilen Test Sırası

1. **İlk test:** GUI ile AAPL, 20 epoch (çok hızlı)
2. **İkinci test:** Web ile TSLA, 30 epoch (grafikler güzel)
3. **Üçüncü test:** Terminal ile MSFT, 50 epoch (tam deneyim)
4. **Karşılaştırma:** Farklı hisseler, aynı ayarlar

---

## 💡 Pro İpuçları

1. **İlk çalıştırmada hata:** Normal, kütüphaneler yükleniyor
2. **İnternet gerekli:** yfinance veri çekmek için
3. **Grafiklere zoom:** Web'de grafiğe tıklayıp sürükleyin
4. **Model kaydet:** Her eğitim `.pth` dosyası oluşturur
5. **Birden fazla eğitim:** Farklı parametrelerle deneyin

Keyifli testler! 🚀
