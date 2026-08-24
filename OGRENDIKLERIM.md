# 📚 Bu Projede Neler Öğrendim?

## 🎓 Genel Bakış

Bu proje boyunca sadece kod yazmakla kalmadım, **derin öğrenme, zaman serisi analizi, veri bilimi ve yazılım geliştirme** konularında kapsamlı deneyim kazandım. İşte öğrendiklerim:

---

## 🧠 1. DERIN ÖĞRENME (Deep Learning)

### PyTorch Framework
- **PyTorch temellerini** öğrendim: tensor işlemleri, autograd, model tanımlama
- **nn.Module** sınıfını kullanarak özel model mimarileri oluşturmayı öğrendim
- **GPU vs CPU** yönetimini anladım (device management)
- **Model kaydetme/yükleme** (checkpoint) mekanizmalarını uyguladım

### LSTM (Long Short-Term Memory)
- **RNN'lerin** neden zaman serileri için önemli olduğunu anladım
- **LSTM'in vanishing gradient problemini** nasıl çözdüğünü öğrendim
- **Cell state ve hidden state** kavramlarını kavradım
- **Sequence-to-one** tahmin mimarisini uyguladım
- **Dropout** ile overfitting'i önlemeyi öğrendim

**Teorik Anlayış:**
```
Normal NN: Geçmişi unutur
RNN: Kısa vadeli hafıza
LSTM: Uzun vadeli hafıza + seçici unutma
→ Hisse senedi gibi trend odaklı veriler için ideal
```

### Model Eğitimi
- **Forward propagation** ve **backward propagation** sürecini anladım
- **Loss function** seçiminin önemini kavradım (neden MSE?)
- **Optimizer** çeşitlerini öğrendim (Adam vs SGD)
- **Learning rate** ayarlamasının etkisini gördüm
- **Batch training** kavramını uyguladım
- **Epoch** sayısının overfitting'e etkisini deneyimledim

**Pratik Deneyim:**
- Learning rate çok yüksek → model diverge oluyor
- Learning rate çok düşük → çok yavaş öğreniyor
- Batch size küçük → daha gürültülü ama genelleşebilir
- Batch size büyük → daha stabil ama bellek tüketiyor

---

## 📊 2. VERİ BİLİMİ VE VERİ İŞLEME

### Veri Toplama
- **API kullanımını** öğrendim (yfinance)
- **Gerçek dünya verisiyle** çalışmanın zorluklarını gördüm
- **Veri kalitesi** kontrolünün önemini anladım
- **Tarih/zaman verisi** yönetimini öğrendim

### Veri Ön İşleme
- **Normalizasyon** neden gerekli? → Sinir ağları büyük sayılarla iyi çalışmaz
- **MinMaxScaler vs StandardScaler** farkını öğrendim
- **Sliding window** tekniğini zaman serileri için uyguladım
- **Train/test split** stratejilerini öğrendim (zaman serilerinde shuffle yok!)

**Önemli Ders:**
```python
# ❌ YANLIŞ: Zaman serilerinde karıştırma
train_test_split(X, y, shuffle=True)

# ✅ DOĞRU: Kronolojik sıra korunmalı
X_train = X[:split_idx]
X_test = X[split_idx:]
```

### NumPy ve Pandas
- **NumPy array** manipülasyonunu öğrendim
- **Pandas DataFrame** işlemlerini kavradım
- **Reshaping** ve **broadcasting** kavramlarını anladım
- **Vektörizasyon** ile performans optimizasyonu yaptım

---

## 📈 3. ZAMAN SERİSİ ANALİZİ

### Zaman Serisi Kavramları
- **Trend, mevsimsellik, gürültü** kavramlarını öğrendim
- **Otokorelasyon** (autocorrelation) nedir anladım
- **Stationarity** (durağanlık) önemini kavradım
- **Lookback window** seçiminin etkisini gördüm

### Finansal Veri Özellikleri
- **Volatilite** yüksek olunca tahmin zorlaşıyor
- **Trend** güçlü olunca model daha başarılı
- **Ani şoklar** (haber, kriz) modeli zorluyor
- **AAPL** gibi istikrarlı hisseler > **TSLA** gibi volatil hisseler (tahmin için)

---

## 🎨 4. YAZILIM GELİŞTİRME

### Proje Yapısı ve Modülerlik
- **Modüler kod** yazmanın önemini anladım
- **Separation of concerns** prensibini uyguladım
- Her modülün tek sorumluluğu olmalı:
  - `data_collection.py` → Sadece veri toplama
  - `model.py` → Sadece model tanımı
  - `train.py` → Sadece eğitim
  - `predict.py` → Sadece tahmin

### Object-Oriented Programming (OOP)
- **Class tasarımı** yaptım (`LSTMStockPredictor`, `StockDataPreprocessor`)
- **Inheritance** kullandım (`nn.Module`'den türetme)
- **Encapsulation** ile kod düzenliliği sağladım
- **Method** ve **attribute** organizasyonu öğrendim

### Arayüz Geliştirme
- **3 farklı arayüz türü** geliştirdim:
  - **CLI** (Command Line Interface) - argparse
  - **GUI** (Graphical User Interface) - Tkinter
  - **Web UI** - Streamlit

**Tkinter ile Öğrendiklerim:**
- Widget'lar (Button, Entry, Label, Frame)
- Layout yönetimi (pack, grid)
- Event handling (button click, callbacks)
- Threading (GUI donmaması için)

**Streamlit ile Öğrendiklerim:**
- Reactive programming
- State management
- Interactive components
- Real-time updates

---

## 📊 5. GÖRSELLEŞTİRME

### Matplotlib
- **Figure ve Axes** kavramlarını öğrendim
- **Çizgi grafikleri** oluşturmayı öğrendim
- **Çoklu subplot** yönetimini kavradım
- **Stil ve renk** özelleştirmesi yaptım
- **Dosyaya kaydetme** (savefig) öğrendim

### Plotly (İnteraktif Grafikler)
- **Plotly Graph Objects** kullandım
- **Hover efektleri** ekledim
- **Zoom ve pan** özellikleri uyguladım
- **Dark theme** stillendirme yaptım

---

## 📏 6. PERFORMANS METRİKLERİ

### Regresyon Metrikleri
Her metriğin ne anlama geldiğini öğrendim:

**MAE (Mean Absolute Error):**
- Ortalama mutlak hata
- Anlaşılması en kolay metrik
- Dolar cinsinden doğrudan yorumlanabilir

**RMSE (Root Mean Squared Error):**
- Büyük hataları daha çok cezalandırır
- MSE'nin karekökü (yorumlanabilir ölçekte)
- Outlier'lara duyarlı

**MAPE (Mean Absolute Percentage Error):**
- Yüzdesel hata
- Farklı ölçekleri karşılaştırmaya yarar
- %5 altı → çok iyi, %10 üstü → zayıf

**R² Score (Coefficient of Determination):**
- Model açıklama gücü (0-1 arası)
- 1.0 = mükemmel, 0.0 = kötü
- 0.7+ → iyi model

**Hangi Metriği Ne Zaman Kullanmalı?**
- Genel performans → **RMSE**
- Hızlı yorumlama → **MAPE**
- Model karşılaştırma → **R²**

---

## 🔧 7. DEBUGGING VE PROBLEM ÇÖZME

### Karşılaştığım Sorunlar ve Çözümler

**Problem 1: Shape Uyumsuzluğu**
```
RuntimeError: Expected input batch_size (32) to match target batch_size (1)
```
**Çözüm:** Tensor shape'lerini doğru ayarlamayı öğrendim
- `.unsqueeze()`, `.squeeze()`, `.reshape()` kullanımı

**Problem 2: Overfitting**
```
Train loss düşüyor ama validation loss artıyor
```
**Çözüm:** 
- Dropout ekleme
- Daha az epoch
- Daha fazla veri

**Problem 3: Vanishing Gradient**
```
Loss azalmıyor, model öğrenmiyor
```
**Çözüm:**
- LSTM kullanımı (RNN yerine)
- Learning rate ayarlama
- Batch normalization

**Problem 4: Çok Yavaş Eğitim**
```
Her epoch 5 dakika sürüyor
```
**Çözüm:**
- Batch size artırma
- DataLoader kullanımı
- GPU kullanımı (mümkünse)

---

## 💻 8. PYTHON İLERİ SEVİYE

### Konular:
- **Type hints** kullanımı
- **Docstring** yazma ("""...""")
- **Exception handling** (try-except)
- **Context managers** (with statement)
- **List comprehension** optimizasyonu
- **F-strings** ile string formatting
- **Argparse** ile CLI oluşturma
- **Threading** ile paralel işlem

### Best Practices:
- PEP 8 kod standardı
- Anlamlı değişken isimleri
- Fonksiyon ve class dokümantasyonu
- DRY (Don't Repeat Yourself) prensibi
- Code readability

---

## 🌐 9. API VE VERİ KAYNAKLARI

### yfinance Kütüphanesi
- **Finansal veri API'si** kullanımını öğrendim
- **Geçmiş veri** vs **canlı veri** farkını anladım
- **Rate limiting** ve **API kotaları** kavramını öğrendim
- **Veri doğrulama** önemini kavradım

**Önemli Ders:**
yfinance gerçek zamanlı değil! Her çalıştırmada güncel verileri çeker ama streaming değil.

---

## 📦 10. PROJE YÖNETİMİ

### Git ve Version Control
- `.gitignore` dosyası oluşturma
- Model dosyalarını (.pth) commit'lememek
- Büyük data dosyalarını yönetme

### Dokümantasyon
- **README.md** yazma
- **Kullanım kılavuzu** oluşturma
- **Kod içi yorum** yazma
- **API documentation** hazırlama

### Dependency Management
- `requirements.txt` oluşturma
- Versiyon pinning (>=2.0.0)
- Sanal ortam (virtual environment) kullanımı

---

## 🎯 11. ALAN BİLGİSİ (Domain Knowledge)

### Finansal Piyasalar
- **Hisse senedi** nasıl çalışır
- **Volatilite** nedir
- **Kapanış fiyatı** (close price) önemi
- **Trend** ve **momentum** kavramları
- Piyasa psikolojisinin etkisi

### Neden Tahmin Zor?
1. **Gürültülü veri** - Rastgele dalgalanmalar
2. **Dış faktörler** - Haberler, politik olaylar
3. **Non-stationary** - İstatistiksel özellikler değişiyor
4. **Kompleks ilişkiler** - Çok değişkenli bağımlılıklar

---

## 🚀 12. YAZILIM MÜHENDİSLİĞİ PRENSİPLERİ

### SOLID Prensipleri
- **S**ingle Responsibility - Her modülün tek görevi
- **O**pen/Closed - Genişletmeye açık, değişime kapalı
- **L**iskov Substitution - Alt sınıf yerine geçebilme
- **I**nterface Segregation - Küçük, spesifik interface'ler
- **D**ependency Inversion - Abstraction'a bağımlılık

### Design Patterns
- **Factory Pattern** - Model oluşturma
- **Strategy Pattern** - Farklı optimizer'lar
- **Observer Pattern** - GUI event handling

---

## 📈 13. PERFORMANS OPTİMİZASYONU

### Öğrendiklerim:
- **Batch processing** verimliliği artırıyor
- **Vektörizasyon** loop'lardan hızlı
- **GPU kullanımı** 10-100x hızlandırma sağlıyor
- **DataLoader** ile paralel veri yükleme
- **Memory management** (tensor deletion, garbage collection)

**Örnek:**
```python
# ❌ Yavaş (loop)
for i in range(len(arr)):
    result[i] = arr[i] * 2

# ✅ Hızlı (vektörizasyon)
result = arr * 2
```

---

## 🧪 14. TEST VE DEBUGGİNG

### Test Stratejileri
- **Küçük veri** ile hızlı test
- **Shape kontrolü** her adımda
- **Sanity check** - Basit durumlar çalışıyor mu?
- **Unit testing** - Her fonksiyon ayrı test

### Debugging Teknikleri
- `print()` debugging
- PyTorch `.shape` kontrolü
- Gradient flow izleme
- Loss tracking ve görselleştirme

---

## 🎨 15. KULLANICI DENEYİMİ (UX)

### Öğrendiklerim:
- **3 farklı kullanıcı tipi** için 3 farklı arayüz
- **Progress feedback** önemli (kullanıcı bekleyebilir)
- **Error messages** açıklayıcı olmalı
- **Visual hierarchy** - Önemli şeyler öne çıkmalı

**Arayüz Seçimi:**
- Teknik kullanıcı → CLI (hızlı, scriptable)
- Normal kullanıcı → GUI (görsel, kolay)
- Demo/paylaşım → Web (erişilebilir, modern)

---

## 💡 16. EN ÖNEMLİ DERSLER

### 1. Küçük Başla, Büyüt
İlk önce basit bir versiyon çalıştır, sonra iyileştir:
```
v1: Sadece model eğitimi
v2: + Veri ön işleme
v3: + Görselleştirme
v4: + GUI
v5: + Web arayüzü
```

### 2. Teoriden Pratiğe Geçiş Zor
- Kaggle notebook okumak ≠ Proje yazmak
- Gerçek veri ≠ Temiz veri
- Hata mesajları ≠ Hata nedeni
- Stack Overflow şart!

### 3. Hiperparametre Tuning = Sanat + Bilim
- Kitaplardaki değerler başlangıç noktası
- Her veri seti farklı
- Deneme-yanılma gerekli
- Sabırlı olmak şart

### 4. Dokümantasyon Kendine Yapılmış İyilik
3 hafta sonra kendi kodumu anlamadım → Dokümantasyon önemli!

### 5. Gerçek Dünya ≠ Tutorial
- Internet kesilince ne olur?
- Veri gelmiyor ise?
- Kullanıcı yanlış girdi yazarsa?
→ Hata yönetimi şart

---

## 🎓 17. KİŞİSEL GELİŞİM

### Teknik Beceriler
- ✅ PyTorch kullanabiliyorum
- ✅ LSTM modellemesi yapabiliyorum
- ✅ Veri pipeline oluşturabiliyorum
- ✅ 3 farklı arayüz geliştirebiliyorum
- ✅ Performans metrikleri yorumlayabiliyorum

### Soft Skills
- ✅ Problem çözme yeteneğim gelişti
- ✅ Dokümantasyon okuma hızlandı
- ✅ Hata ayıklama becerim arttı
- ✅ Büyük proje yönetimi deneyimi kazandım
- ✅ Kullanıcı düşünerek tasarım yapabiliyorum

### Öğrenme Kaynakları
- PyTorch documentation
- Stack Overflow
- Kaggle notebooks
- Medium makaleleri
- YouTube tutorialları
- Research paper'lar (LSTM, attention)

---

## 🚀 18. BUNDAN SONRAKİ ADIMLAR

### Öğrenmek İstediklerim:
1. **Transformer modelleri** - Attention mechanism
2. **GRU** (Gated Recurrent Unit) - LSTM alternatifi
3. **Ensemble learning** - Birden fazla model kombinasyonu
4. **Feature engineering** - Volume, indicators ekleme
5. **Sentiment analysis** - Haber/sosyal medya analizi
6. **Reinforcement learning** - Trading bot geliştirme
7. **Model deployment** - Production ortamına alma
8. **A/B testing** - Model karşılaştırma

### Proje Geliştirmeleri:
- [ ] Çoklu özellik ekleme (OHLCV)
- [ ] 7 gün ileriye tahmin
- [ ] Real-time streaming veri
- [ ] Çoklu hisse portföyü
- [ ] Risk analizi ekleme
- [ ] Backtesting sistemi
- [ ] REST API geliştirme
- [ ] Docker containerization

---

## 📊 19. İSTATİSTİKSEL DÜŞÜNME

### Öğrendiklerim:
- **Korelasyon ≠ Nedensellik**
- **Overfitting** tehlikesi her zaman var
- **Bias-variance tradeoff** dengelemek zor
- **Test seti** hiç görülmemeli (data leakage)
- **Cross-validation** zaman serilerinde farklı

---

## 💭 20. FELSEFİ DERSLER

### AI ve Finans
- Yapay zeka her şeyi çözemez
- Model tahmin yapar, karar vermez
- %100 doğruluk imkansız (piyasalar kaotik)
- Etik kullanım önemli (yatırım tavsiyesi değil)

### Öğrenme Süreci
- Hata yapmak öğrenmenin parçası
- Her hata bir ders
- Sürekli öğrenme gerekli (AI hızla gelişiyor)
- Topluluk önemli (Stack Overflow, GitHub)

---

## 🎯 ÖZET

Bu proje sayesinde:

✅ **Derin öğrenme** temellerini uygulamalı öğrendim
✅ **LSTM** mimarisini gerçek problemde kullandım
✅ **Veri bilimi** pipeline'ı kurdum (toplama → işleme → modelleme)
✅ **PyTorch** framework'ünde ustalaştım
✅ **3 farklı arayüz** geliştirdim
✅ **Yazılım mühendisliği** prensiplerini uyguladım
✅ **Performans metrikleri** yorumlamayı öğrendim
✅ **Gerçek dünya verileri** ile çalıştım
✅ **Problem çözme** becerilerimi geliştirdim
✅ **Dokümantasyon** yazmanın önemini anladım

**En önemli ders:** Kitaplardan okumak ≠ Yapmak. Gerçek öğrenme, elini kirletip kod yazınca, hatalar yapınca, debug ederken oluyor!

---

## 📚 Tavsiyelerim (Kendime ve Başkalarına)

1. **Küçük başla** - İlk önce çalışan bir şey yap
2. **Dokümante et** - 1 hafta sonra unutuyorsun
3. **Test et** - Her şeyi test et
4. **Modüler yaz** - Spagetti kod'dan kaç
5. **Öğrenmeye devam et** - AI dünyası hızla değişiyor
6. **Paylaş** - GitHub'a koy, başkalarından öğren
7. **Sabırlı ol** - Öğrenme zaman alıyor
8. **Eğlen** - Zorlanınca mola ver, geri dön

**Bu sadece başlangıç. Öğrenme yolculuğu devam ediyor!** 🚀
