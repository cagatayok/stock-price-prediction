# ⚡ HIZLI TEST KILAVUZU - 3 Dakikada Hazır

## 🎯 Sunumdan Önce Test Et

### ✅ Adım 1: Klasöre Git (5 saniye)
```bash
cd Desktop/mcirosoft
```

### ✅ Adım 2: Hızlı Komut Testi (2 dakika)
```bash
python main.py --ticker AAPL --epochs 10
```

**Beklenen çıktı:**
```
############################################################
#  HİSSE SENEDİ FİYAT TAHMİN SİSTEMİ
############################################################
📊 AAPL için veri indiriliyor...
✅ 1255 veri noktası indirildi
🔄 Veri işleniyor...
🧠 Model oluşturuluyor...
🎯 Eğitim yapılıyor...
Epoch [ 10/10] | Train Loss: ... | Val Loss: ...
✅ EĞİTİM TAMAMLANDI!
📊 RMSE: $...
```

**Süre:** ~1-2 dakika

**✅ BAŞARILI!** → Komut satırı çalışıyor

---

### ✅ Adım 3: GUI Testi (1 dakika)
```bash
python app_gui.py
```

**Beklenen:**
- Dark theme pencere açılmalı
- Sol panelde ayarlar görünmeli
- Sağ panelde log alanı olmalı

**Test et:**
1. Hisse: AAPL
2. Epoch: 10
3. "🚀 Eğitimi Başlat" tıkla
4. 1-2 dakika bekle
5. Sonuçlar görünmeli

**✅ BAŞARILI!** → GUI çalışıyor

---

### ✅ Adım 4: Web Testi (1 dakika)
```bash
python -m streamlit run app_web.py
```

**Tarayıcıda otomatik açılır:** `http://localhost:8501`

**Beklenen:**
- Modern, dark theme sayfa
- Sol sidebar (ayarlar)
- Ana bölümde hoş geldin ekranı

**Test et:**
1. Sol menüden AAPL seçili
2. Epoch slider'ı 10'a çek
3. "🚀 Eğitimi Başlat" tıkla
4. Progress bar ilerlemeli
5. Grafikler oluşmalı

**✅ BAŞARILI!** → Web çalışıyor

---

## 🎬 SUNUM SIRASINDA

### Seçenek A: Önceden Hazır Grafikler (EN GÜVENLİ)

**Neden:** Canlı demo riskli (internet, hata vb.)

**Nasıl:**
1. Önceden çalıştırılmış grafikleri aç:
   - `AAPL_predictions.png`
   - `AAPL_training_history.png`
   - `TSLA_predictions.png`

2. Sunumda göster ve anlat

3. "Şimdi size kodu göstereyim" de, dosyaları aç

---

### Seçenek B: Web Demo (ORTA RİSK)

**Neden:** Modern görünüyor, interaktif

**Nasıl:**

**SUNUM ÖNCESI:**
```bash
# Terminal'de başlat
python -m streamlit run app_web.py
```

**SUNUM SIRASINDA:**
1. Tarayıcıyı aç: `http://localhost:8501`
2. Ekranı paylaş
3. Sol menüden AAPL seç
4. Epoch: 30 (hızlı olsun)
5. "Eğitimi Başlat" tıkla
6. Beklerken kodu anlatabilirsin
7. 2-3 dakika sonra sonuçlar

---

### Seçenek C: Terminal Demo (DÜŞÜK RİSK)

**Neden:** Hızlı, profesyonel görünüyor

**Nasıl:**

**SUNUM SIRASINDA:**
```bash
# Terminal'i aç, ekranı paylaş
python main.py --ticker AAPL --epochs 20
```

2-3 dakika beklerken:
- Mimariyi anlat
- Kodu göster
- Grafikleri aç

---

## 🆘 SORUN ÇÖZME (Acil!)

### Sorun 1: "python komutu bulunamadı"
```bash
# Çözüm:
python3 main.py
# veya
py main.py
```

### Sorun 2: "ModuleNotFoundError"
```bash
# Çözüm (hızlıca):
pip install -r requirements.txt
```

### Sorun 3: Web açılmıyor
```bash
# Çözüm:
# Başka port dene
streamlit run app_web.py --server.port 8502
```

### Sorun 4: Çok yavaş
```bash
# Çözüm:
# Epoch azalt
python main.py --ticker AAPL --epochs 10
```

### Sorun 5: İnternet yok (veri indirilemiyor)
**Çözüm:**
- Önceden hazırladığınız grafikleri gösterin
- "Önceden eğitilmiş model" deyin

---

## 📋 SUNUM ÖNCESİ CHECKLIST

### 5 Dakika Önce:

- [ ] **Terminal açık** (doğru klasörde)
- [ ] **Hızlı test yaptım** (10 epoch ile)
- [ ] **Grafikler hazır** (backup olarak)
- [ ] **İnternet var** (veri için)
- [ ] **Web çalışıyor** (localhost:8501)
- [ ] **Kod editör açık** (göstermek için)

### Ekstra Hazırlık:

- [ ] **AAPL.png** açık (en iyi sonuç)
- [ ] **TSLA.png** açık (karşılaştırma için)
- [ ] **model.py** açık (kod göstermek için)
- [ ] **README.md** açık (genel bakış)

---

## 🎯 TEST SENARYOLARı (Seçin)

### Senaryo 1: Sadece Grafikler (0 risk)
```
Süre: 5 dakika
Risk: Yok
Etki: Orta

Adımlar:
1. Önceden hazır grafikleri göster
2. Sonuçları anla
3. Kodu göster
4. Bitti
```

### Senaryo 2: Web Demo (Düşük risk)
```
Süre: 8 dakika
Risk: Düşük
Etki: Yüksek

Adımlar:
1. Tarayıcıda localhost:8501 aç
2. Canlı eğitim başlat (30 epoch)
3. Beklerken kodu göster
4. Sonuçları göster
```

### Senaryo 3: Terminal Demo (Orta risk)
```
Süre: 10 dakika
Risk: Orta
Etki: Yüksek

Adımlar:
1. Terminal'de komut çalıştır
2. Log akışını göster
3. Grafikleri aç
4. Farklı hisse dene (TSLA)
```

---

## 💡 PRO İPUCLARI

### İpucu 1: Yedek Plan
```
Plan A: Canlı demo
Plan B: Önceden hazır grafikler
Plan C: Sadece kod göster + anlatım
```

### İpucu 2: Zaman Yönetimi
```
Demo çok uzun sürüyorsa:
- "Beklerken size mimariyi anlatayım"
- "Burada eğitim devam ederken..."
- "İsterseniz sonuçları önceden hazırladığım grafiklerde göstereyim"
```

### İpucu 3: Hata Durumunda
```
Hata çıkarsa PANIĞE KAPILMA:
- "İnternet bağlantısı nedeniyle..."
- "Şimdi size önceki sonuçları göstereyim"
- "Kod burada çalışıyor, mimariyi göstereyim"
```

---

## 🚀 HIZLI BAŞLATMA KOMUTLARI

Sunum başlamadan önce terminalde hazır bulundur:

### Terminal 1:
```bash
cd Desktop/mcirosoft
# Hazır bekle
```

### Terminal 2:
```bash
cd Desktop/mcirosoft
python -m streamlit run app_web.py
# Web çalışır durumda
```

### Tarayıcı:
```
http://localhost:8501
# Açık tab'da beklet
```

### Grafikler:
```
AAPL_predictions.png - Açık
TSLA_predictions.png - Açık  
AAPL_training_history.png - Açık
```

---

## ⏱️ ÖRNEK ZAMAN ÇİZELGESİ

### 5 Dakikalık Sunum:
```
00:00-01:00 → Giriş ve problem
01:00-02:00 → Grafikleri göster (önceden hazır)
02:00-03:30 → Teknik açıklama
03:30-05:00 → Sonuç ve soru
```

### 10 Dakikalık Sunum:
```
00:00-01:00 → Giriş
01:00-02:00 → Mimari açıklama
02:00-05:00 → Canlı web demo (eğitim başlat)
05:00-07:00 → Grafik analizi
07:00-08:00 → Kod göster
08:00-10:00 → Sonuç ve soru
```

---

## 📞 YEDEK İLETİŞİM

Sunumda sorun olursa:

1. **Grafikleri göster** (her zaman çalışır)
2. **Kodu aç** (VS Code'da)
3. **Mimariyi anlat** (tahta/slayt)
4. **Daha önce çalıştığını söyle** (doğru)

---

## ✅ SON KONTROL (1 dakika önce)

```bash
# Hızlı test:
python main.py --ticker AAPL --epochs 5

# Çıktı geliyorsa:
✅ HER ŞEY HAZIR!

# Hata varsa:
❌ Grafikleri göster (Plan B)
```

**Başarılar! Rahat ol, projen harika! 🚀**
