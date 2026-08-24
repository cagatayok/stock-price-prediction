# 📚 Hisse Senedi Fiyat Tahmini - Kullanım Kılavuzu

## 🎯 3 Farklı Kullanım Yöntemi

### 1️⃣ Komut Satırı (Terminal)

En basit ve hızlı yöntem:

```bash
# Varsayılan ayarlarla (Apple hissesi)
python main.py

# Özel ayarlarla
python main.py --ticker TSLA --epochs 100 --hidden-size 128
```

**Parametreler:**
- `--ticker` : Hisse sembolü (AAPL, TSLA, GOOGL, MSFT vb.)
- `--period` : Veri periyodu (1y, 2y, 5y, 10y)
- `--lookback` : Geçmiş pencere günü (30-120 arası)
- `--hidden-size` : LSTM boyutu (32, 64, 128, 256)
- `--num-layers` : LSTM katman sayısı (1-3 arası)
- `--epochs` : Eğitim döngüsü (10-200 arası)
- `--batch-size` : Batch boyutu (16, 32, 64, 128)
- `--learning-rate` : Öğrenme oranı (0.0001-0.01 arası)

---

### 2️⃣ Grafiksel Arayüz (Tkinter GUI)

Masaüstü uygulaması:

```bash
python app_gui.py
```

**Özellikler:**
- ✅ Kolay kullanımlı arayüz
- ✅ Canlı eğitim logları
- ✅ Progress bar ile ilerleme takibi
- ✅ Tek tıkla sonuçları açma
- ✅ Eğitimi durdurma özelliği

**Nasıl Kullanılır:**
1. Sol panelden parametreleri ayarlayın
2. "🚀 Eğitimi Başlat" butonuna tıklayın
3. Sağ taraftaki loglarda ilerlemeyi izleyin
4. Eğitim bitince "📊 Sonuçları Aç" ile grafikleri görün

---

### 3️⃣ Web Arayüzü (Streamlit)

Modern, interaktif web uygulaması:

```bash
python -m streamlit run app_web.py
```

Tarayıcınızda otomatik açılır: **http://localhost:8501**

**Özellikler:**
- ✅ Modern, responsive tasarım
- ✅ İnteraktif grafikler (Plotly)
- ✅ Canlı metrik göstergeler
- ✅ Popüler hisseler için hızlı butonlar
- ✅ Koyu tema
- ✅ Mobil uyumlu

**Nasıl Kullanılır:**
1. Sol sidebar'dan ayarları yapın
2. "🚀 Eğitimi Başlat" butonuna tıklayın
3. Sayfada canlı olarak sonuçları görün
4. İnteraktif grafiklerde zoom yapabilirsiniz

---

## 📊 Veri Hakkında

### ⚠️ ÖNEMLİ: Veri Çekme Açıklaması

**yfinance API'si:**
- ✅ **Gerçek hisse senedi verileri** çeker
- ✅ **Geçmiş verileri** indirir (günlük kapanış fiyatları)
- ✅ Her çalıştırmada **en güncel verileri** alır
- ❌ **Canlı/anlık (live) değil** - sadece geçmiş veriler
- ❌ **Real-time streaming yok** - batch indirme

**Örnek:**
- `period="5y"` → Son 5 yılın günlük verileri
- `period="1y"` → Son 1 yılın günlük verileri
- Her gün yeni bir kapanış fiyatı eklenir

**Canlı Veri İsterseniz:**
- WebSocket API'leri kullanmanız gerekir (örn: Binance, Alpaca)
- Ücretli finansal data provider'lar (Bloomberg, Reuters)
- yfinance sadece eğitim/test için uygundur

---

## 🧪 Test Senaryoları

### Hızlı Test (2-3 dakika)
```bash
python main.py --ticker AAPL --epochs 20 --batch-size 64
```

### Orta Seviye Test (5-10 dakika)
```bash
python main.py --ticker TSLA --epochs 100 --hidden-size 128 --num-layers 2
```

### Güçlü Model (15-20 dakika)
```bash
python main.py --ticker GOOGL --epochs 200 --hidden-size 256 --num-layers 3 --lookback 90
```

---

## 📈 Sonuçları Anlama

### Performans Metrikleri

**RMSE (Root Mean Squared Error)**
- Ortalama tahmin hatası (dolar cinsinden)
- Düşük = daha iyi
- Örnek: $10 RMSE → ortalama $10 hata

**MAE (Mean Absolute Error)**
- Mutlak hataların ortalaması
- Düşük = daha iyi
- RMSE'den daha kolay yorumlanır

**MAPE (Mean Absolute Percentage Error)**
- Yüzdesel hata oranı
- %3-5 arası → çok iyi
- %5-10 arası → iyi
- %10+ → orta/zayıf

**R² Score (Coefficient of Determination)**
- Model açıklama gücü (0-1 arası)
- 1.0 = mükemmel tahmin
- 0.9+ = çok iyi
- 0.7-0.9 = iyi
- 0.5-0.7 = orta
- 0.5 altı = zayıf

---

## 📁 Çıktı Dosyaları

Her eğitim sonrası oluşur:

1. **`{TICKER}_model.pth`**
   - Eğitilmiş PyTorch modeli
   - Yeniden kullanılabilir

2. **`{TICKER}_predictions.png`**
   - Gerçek vs Tahmin grafiği
   - Tüm test verisi

3. **`{TICKER}_predictions_zoomed.png`**
   - Yakınlaştırılmış görünüm
   - İlk 100 test örneği

4. **`{TICKER}_training_history.png`**
   - Eğitim kayıp grafiği
   - Overfitting kontrolü için

---

## 🔧 Sorun Giderme

### "pip not found" Hatası
```bash
python -m pip install -r requirements.txt
```

### "yfinance no data" Hatası
- Hisse sembolünü kontrol edin (büyük harf olmalı)
- İnternet bağlantınızı kontrol edin
- Geçerli bir sembol olduğundan emin olun

### Yavaş Eğitim
- Epoch sayısını azaltın
- Batch size'ı artırın (32 → 64)
- Hidden size'ı azaltın (128 → 64)

### Kötü Performans
- Epoch sayısını artırın (50 → 100+)
- Lookback penceresini ayarlayın
- Farklı hidden size deneyin
- Learning rate'i değiştirin

---

## 💡 İpuçları

1. **İlk Defa Kullanım:** Küçük parametrelerle başlayın
   ```bash
   python main.py --ticker AAPL --epochs 20
   ```

2. **GPU Varsa:** Otomatik kullanılır, ek ayar gerekmez

3. **Farklı Hisseler:** Volatilite farklı olduğu için sonuçlar değişir
   - AAPL → genelde düşük volatilite → iyi sonuç
   - TSLA → yüksek volatilite → zor tahmin

4. **Overfitting Kontrolü:** Training loss < Validation loss ise sorun yok

5. **Sonuçları Karşılaştırma:** Farklı parametrelerle eğitin ve karşılaştırın

---

## 🎓 Öğrenme Kaynakları

- PyTorch Dokümantasyonu: https://pytorch.org/docs/
- LSTM Açıklaması: https://colah.github.io/posts/2015-08-Understanding-LSTMs/
- yfinance Docs: https://pypi.org/project/yfinance/

---

## 📞 Destek

Sorularınız için GitHub issues kullanın veya kodu inceleyin:
- `model.py` - LSTM mimarisi
- `train.py` - Eğitim döngüsü
- `data_preprocessing.py` - Veri hazırlama
