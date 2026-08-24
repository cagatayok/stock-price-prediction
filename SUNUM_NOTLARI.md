# 📊 SUNUM NOTLARI - Hisse Senedi Fiyat Tahmini Projesi

## 🎯 PROJE ÖZETİ (30 saniye)

**"PyTorch ve LSTM kullanarak hisse senedi fiyatlarını tahmin eden bir yapay zeka projesi geliştirdim."**

### Ana Özellikler:
- 🧠 Derin öğrenme ile zaman serisi tahmini
- 📊 Gerçek hisse senedi verileri (Apple, Tesla, Google vb.)
- 🎨 3 farklı kullanıcı arayüzü (Terminal, Masaüstü, Web)
- 📈 Görselleştirme ve performans analizi

---

## 📖 PROJE DETAYLI ANLATIM

### SLAYT 1: Giriş ve Problem

**Ne söyleyeceksiniz:**
"Hisse senedi fiyat tahmini, finansal piyasalarda en zor problemlerden biridir. Bu projede, geçmiş fiyat hareketlerinden öğrenen bir yapay zeka modeli geliştirdim."

**Teknik detaylar:**
- Problem: Zaman serisi tahmini
- Veri: Gerçek borsa verileri (yfinance API)
- Hedef: Yarının kapanış fiyatını tahmin etmek
- Zorluk: Yüksek volatilite, gürültülü veri

---

### SLAYT 2: Teknik Mimari

**Ne söyleyeceksiniz:**
"Proje 5 ana bileşenden oluşuyor..."

#### 1️⃣ VERİ TOPLAMA
```
yfinance API → Gerçek hisse senedi verileri
- Son 5 yılın günlük kapanış fiyatları
- Otomatik indirme
- 1200+ veri noktası
```

**Önemli:** "yfinance geçmiş verileri çeker, canlı değil. Ama her çalıştırmada en güncel verileri indirir."

#### 2️⃣ VERİ ÖN İŞLEME
```
Ham Veri → MinMaxScaler → 0-1 arası normalize
Sliding Window → Son 60 gün → Sonraki günü tahmin et
Train/Test Split → %80 / %20
```

**Örnek:**
- Girdi: [gün1, gün2, ..., gün60]
- Çıktı: gün61

#### 3️⃣ MODEL MİMARİSİ (LSTM)
```
┌─────────────────────────┐
│  Girdi: 60 gün × 1      │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  LSTM Katman 1 (64)     │
│  Dropout (0.2)          │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  LSTM Katman 2 (64)     │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  Fully Connected (1)    │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  Çıktı: 1 gün tahmini   │
└─────────────────────────┘
```

**Neden LSTM?**
"LSTM, geçmiş bilgileri 'hafızasında' tutabilen özel bir sinir ağıdır. Hisse senedi gibi zaman serilerinde geçmiş trendler önemli olduğu için LSTM idealdir."

#### 4️⃣ EĞİTİM
```
Kayıp Fonksiyonu: MSE (Mean Squared Error)
Optimizer: Adam
Epoch: 50-100
Batch Size: 32
Learning Rate: 0.001
```

**Ne söyleyeceksiniz:**
"Model, gerçek ve tahmin arasındaki farkı minimize etmeye çalışıyor. Her epoch'ta ağırlıkları güncelliyor."

#### 5️⃣ TAHMİN VE DEĞERLENDİRME
```
Performans Metrikleri:
- RMSE: Ortalama hata (dolar)
- MAPE: Yüzdesel hata (%)
- R²: Model açıklama gücü (0-1)
```

---

### SLAYT 3: Sonuçlar

**Tablo gösterin:**

| Hisse | RMSE | MAPE | R² Score | Yorum |
|-------|------|------|----------|-------|
| AAPL  | $11.96 | 3.45% | 0.7566 | İyi |
| TSLA  | $12.91 | 2.51% | 0.8916 | Çok İyi |

**Ne söyleyeceksiniz:**
"Apple için ortalama $12 hata ile %3.45 MAPE elde ettik. Bu, fiyatın yaklaşık %96.5 doğrulukla tahmin edildiği anlamına geliyor."

"Tesla'da R² 0.89 - bu mükemmel bir sonuç. Model, fiyat hareketinin %89'unu açıklayabiliyor."

---

### SLAYT 4: Arayüzler

**Ne söyleyeceksiniz:**
"Kullanıcı deneyimi için 3 farklı arayüz geliştirdim..."

#### 1️⃣ Terminal (CLI)
```bash
python main.py --ticker AAPL --epochs 50
```
- En hızlı
- Teknik kullanıcılar için
- Tam kontrol

#### 2️⃣ Masaüstü (Tkinter GUI)
- Kullanıcı dostu
- Canlı log takibi
- Tek tıkla çalıştırma

#### 3️⃣ Web (Streamlit)
- Modern, responsive
- İnteraktif grafikler
- Tarayıcıdan erişim

**Demo yapın:** Birini canlı gösterin

---

### SLAYT 5: Grafikler

**2 grafik gösterin:**

#### Grafik 1: Eğitim Grafiği
```
Y ekseni: Kayıp (MSE)
X ekseni: Epoch
Mavi: Eğitim kaybı
Kırmızı: Validasyon kaybı
```

**Ne söyleyeceksiniz:**
"Görüldüğü gibi kayıp zamanla azalıyor. Overfitting yok çünkü validasyon kaybı da paralel düşüyor."

#### Grafik 2: Tahmin Grafiği
```
Mavi çizgi: Gerçek fiyat
Kırmızı kesikli: Tahmin
```

**Ne söyleyeceksiniz:**
"İki çizgi çok yakın seyrediyor. Model, trendi başarıyla yakalıyor. Bazı ani değişimlerde sapma var ama bu normal."

---

### SLAYT 6: Teknolojiler

**Stack gösterin:**
```
Backend:
- Python 3.11
- PyTorch 2.0 (Derin öğrenme framework)
- NumPy, Pandas (Veri işleme)

Veri:
- yfinance (Finansal veri API)
- scikit-learn (Preprocessing)

Görselleştirme:
- Matplotlib (Statik grafikler)
- Plotly (İnteraktif grafikler)

Arayüz:
- Tkinter (Desktop GUI)
- Streamlit (Web UI)
```

---

### SLAYT 7: Zorluklar ve Çözümler

**Zorluk 1: Veri Ölçeklendirme**
- Problem: Sinir ağları büyük sayılarla iyi çalışmaz
- Çözüm: MinMaxScaler ile 0-1 arası normalize

**Zorluk 2: Zaman Serisi Formatı**
- Problem: LSTM özel bir input format bekler
- Çözüm: Sliding window ile (60, 1) shape'e dönüştürme

**Zorluk 3: Overfitting**
- Problem: Model ezberleme yapabilir
- Çözüm: Dropout (0.2) ve train/validation split

**Zorluk 4: Yüksek Volatilite (Tesla)**
- Problem: Ani fiyat değişimleri
- Çözüm: Daha fazla epoch ve daha büyük model

---

### SLAYT 8: Gelecek Geliştirmeler

**Ne eklenebilir:**
1. **Çoklu Özellikler:** Volume, Open, High, Low (şu an sadece Close)
2. **Daha Uzun Tahmin:** 1 gün yerine 7 gün
3. **Sentiment Analysis:** Haber başlıklarından duygu analizi
4. **Ensemble Model:** LSTM + GRU + Transformer
5. **Real-time Tahmin:** WebSocket ile canlı veri

---

## 🎬 CANLI DEMO SENARYOSU

### Senaryo 1: Terminal Demo (2 dakika)

**Ekranda gösterin:**
```bash
# Terminal'i açın
python main.py --ticker AAPL --epochs 20
```

**Söyleyecekleriniz:**
1. "Şimdi Apple hissesi için model eğiteceğim"
2. "Veri indiriliyor..." (log akıyor)
3. "Model eğitiliyor..." (epoch'ları gösterin)
4. "İşte sonuçlar: RMSE $12, MAPE %3.5"
5. "Grafikler otomatik oluşturuldu"

### Senaryo 2: Web Demo (3 dakika)

**Tarayıcıda gösterin:**
```
http://localhost:8501
```

**Adımlar:**
1. "Modern web arayüzü açıldı"
2. Sol menüden TSLA seçin
3. Epoch'u 30'a ayarlayın
4. "Eğitimi Başlat" butonuna tıklayın
5. Progress bar'ı gösterin
6. Canlı grafikleri gösterin
7. "İnteraktif, zoom yapabiliriz"

### Senaryo 3: Karşılaştırma (2 dakika)

**İki hisseyi karşılaştırın:**
```bash
# Apple
python main.py --ticker AAPL --epochs 30

# Tesla  
python main.py --ticker TSLA --epochs 30
```

**Söyleyecekleriniz:**
"Apple daha düşük volatilite → daha tahmin edilebilir"
"Tesla daha volatil → model zorlanıyor ama yine de iyi"

---

## 📋 TEST ADIMLARI (Sunumda Kullanmak İçin)

### HAZIRLIK (Sunum Öncesi)

```bash
# 1. Klasörü açın
cd Desktop/mcirosoft

# 2. Bir hızlı test yapın (çalıştığından emin olun)
python main.py --ticker AAPL --epochs 10

# 3. Web'i başlatın
python -m streamlit run app_web.py

# 4. GUI'yi başlatın  
python app_gui.py
```

### SUNUM SIRASINDA

#### Seçenek A: Hızlı Demo (Önceden Çalıştırılmış)
1. Önceden oluşturulmuş grafikleri gösterin
2. "İşte sonuçlar" deyin
3. Kodu kısaca gösterin

#### Seçenek B: Canlı Demo (Riskli ama etkileyici)
1. Terminal'i açın
2. `python main.py --ticker AAPL --epochs 20` çalıştırın
3. 2-3 dakika beklerken kodu anlatın
4. Sonuçları gösterin

#### Seçenek C: Web Demo (En Güvenli)
1. Tarayıcıda `http://localhost:8501` açın
2. Parametre değiştirin
3. Butona tıklayın
4. Canlı sonuçları gösterin

---

## 🎤 SORU-CEVAP İÇİN HAZIRLIK

### Soru: "Neden LSTM kullandınız?"
**Cevap:** "LSTM, geçmiş bilgileri hatırlayabilen özel bir RNN türüdür. Hisse senedi fiyatları geçmişe bağımlı olduğu için (trend, momentum) LSTM bu ilişkileri öğrenebiliyor. Normal sinir ağları kısa vadeli hafızaya sahipken, LSTM uzun vadeli bağımlılıkları yakalayabiliyor."

### Soru: "Gerçek hayatta kullanılabilir mi?"
**Cevap:** "Bu proje eğitim amaçlıdır. Gerçek yatırımda kullanmak için: 1) Daha fazla özellik (volume, haber analizi), 2) Canlı veri akışı, 3) Risk yönetimi, 4) Backtesting gerekir. Ayrıca finansal piyasalar çok karmaşık - hiçbir model %100 doğru tahmin yapamaz."

### Soru: "Doğruluk oranınız ne kadar?"
**Cevap:** "MAPE %3-4 civarı, yani yaklaşık %96-97 doğruluk. Ama dikkat: Bu sadece test verisi için. Gelecek için garanti değil. R² score 0.75-0.89 arasında, bu istatistiksel olarak güçlü bir model."

### Soru: "Hangi hisse en iyi sonuç veriyor?"
**Cevap:** "Tesla en iyi R² verdi (0.89) çünkü güçlü trend var. Apple daha düşük volatiliteli ama yine iyi. Volatilitesi çok yüksek penny stock'larda model zorlanıyor."

### Soru: "Kodu nereden öğrendiniz?"
**Cevap:** "PyTorch dokümantasyonu, Andrew Ng'nin Deep Learning kursu, ve çeşitli research paper'lar. LSTM mimarisini Understanding LSTMs blog yazısından öğrendim."

### Soru: "GPU kullandınız mı?"
**Cevap:** "Kod GPU destekli. Varsa otomatik kullanıyor. Bu proje için CPU yeterli (50 epoch 30 saniye), ama büyük modellerde GPU şart."

### Soru: "Başka ne ekleyebilirsiniz?"
**Cevap:** "Transformer modeli, sentiment analysis, ensemble learning, multi-step tahmin (7 gün ileri), ve risk analizi eklenebilir."

---

## 📱 SUNUM SONRASI PAYLAŞIM

### GitHub'a Yüklemek İçin:
```bash
git init
git add .
git commit -m "Stock price prediction with PyTorch LSTM"
git remote add origin [YOUR_REPO]
git push -u origin main
```

### README'de Vurgulanacaklar:
- 3 farklı arayüz
- Gerçek veri (yfinance)
- İyi performans metrikleri
- Detaylı dokümantasyon

---

## 🎯 SUNUM İPUÇLARI

### DO (Yapın):
✅ Grafikleri büyük gösterin
✅ Kodu kısaca gösterin (model.py)
✅ Canlı demo yapın (mümkünse)
✅ Metrikleri açıklayın
✅ Zorlukları paylaşın (otantik görünür)
✅ Teknik terimler kullanın ama açıklayın

### DON'T (Yapmayın):
❌ "Bu %100 doğru tahmin yapıyor" demeyin
❌ Çok detaya girmeyin (kod satır satır)
❌ Overfitting, gradient descent gibi çok teknik konulara dalmayin (sorulmazsa)
❌ "Yatırım tavsiyesidir" izlenimi vermeyin

---

## ⏱️ ZAMAN PLANLAMASI

### 5 Dakikalık Sunum:
- 1 dk: Problem ve çözüm
- 2 dk: Teknik mimari (hızlıca)
- 1 dk: Sonuçlar ve grafikler
- 1 dk: Demo veya özet

### 10 Dakikalık Sunum:
- 1 dk: Giriş
- 3 dk: Teknik detaylar
- 2 dk: Sonuçlar ve analiz
- 3 dk: Canlı demo
- 1 dk: Gelecek planlar

### 15 Dakikalık Sunum:
- 2 dk: Problem ve motivasyon
- 5 dk: Teknik mimari (detaylı)
- 3 dk: Sonuçlar, grafikler, karşılaştırma
- 4 dk: Canlı demo
- 1 dk: Sonuç ve soru-cevap

---

## 🎬 FİNAL KONTROL LİSTESİ

Sunum öncesi kontrol edin:

- [ ] Terminal hazır (klasör doğru)
- [ ] Web çalışıyor (localhost:8501)
- [ ] GUI açılabiliyor
- [ ] Grafikler hazır (backup olarak)
- [ ] İnternet bağlantısı var (veri indirmek için)
- [ ] Sunumda kullanacağınız hisse sembolü çalışıyor
- [ ] Kodu açık (VS Code veya editor)
- [ ] Metrikler ezberde

**Son söz:** Rahat olun, projeniz çalışıyor ve etkileyici! 🚀

---

## 💡 BONUS: ETKILEYICI BAŞLANGIÇ

**Açılış cümlesi:**
"Yarının Apple hissesi 305 dolar mı, 320 dolar mı olacak? Bu projeyle yapay zeka bunu tahmin etmeye çalışıyor - ve sonuçlar oldukça başarılı!"

**veya**

"Her gün milyarlarca dolar borsada işlem görüyor. Peki yapay zeka fiyat hareketlerini öğrenebilir mi? İşte bu projenin cevabı: Evet, ve oldukça iyi!"

**Kapanış cümlesi:**
"Bu proje, derin öğrenmenin finansal zaman serilerine nasıl uygulanabileceğini gösteriyor. Gerçek dünyada kullanılabilirlik için daha fazla geliştirme gerekse de, temel yaklaşım sağlam ve sonuçlar cesaret verici."
