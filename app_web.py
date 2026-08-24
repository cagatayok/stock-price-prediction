"""
Hisse Senedi Fiyat Tahmini - Web Arayüzü (Streamlit)
"""
import streamlit as st
import torch
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

from data_collection import download_stock_data, get_close_prices
from data_preprocessing import StockDataPreprocessor
from model import LSTMStockPredictor
from train import StockModelTrainer
from predict import make_predictions, calculate_metrics
from trading_signals import TradingSignalGenerator


# Sayfa yapılandırması
st.set_page_config(
    page_title="Hisse Senedi Fiyat Tahmini",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #007acc;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #005a9e;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #007acc;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """
    Ana uygulama
    """
    # Başlık
    st.title("📈 Hisse Senedi Fiyat Tahmini")
    st.markdown("### PyTorch LSTM ile Derin Öğrenme")
    st.markdown("---")
    
    # Bilgi mesajı
    st.info("⚠️ **Not:** yfinance API'si **geçmiş verileri** çeker. Her çalıştırmada en güncel veriler indirilir (günlük kapanış fiyatları).")
    
    # Sidebar - Ayarlar
    with st.sidebar:
        st.header("⚙️ Model Ayarları")
        
        # Hisse Sembolü
        ticker = st.text_input(
            "Hisse Sembolü",
            value="AAPL",
            help="Örnek: AAPL, TSLA, GOOGL, MSFT"
        ).upper()
        
        # Periyot
        period = st.selectbox(
            "Veri Periyodu",
            options=["1y", "2y", "3y", "5y", "10y"],
            index=3,
            help="Ne kadar geçmiş veri çekileceği"
        )
        
        st.markdown("---")
        st.subheader("🧠 Model Parametreleri")
        
        # Lookback
        lookback = st.slider(
            "Geçmiş Pencere (gün)",
            min_value=30,
            max_value=120,
            value=60,
            step=10,
            help="Model kaç günlük geçmişe bakacak"
        )
        
        # Hidden Size
        hidden_size = st.selectbox(
            "LSTM Gizli Katman Boyutu",
            options=[32, 64, 128, 256],
            index=1,
            help="Daha büyük = daha güçlü model"
        )
        
        # Num Layers
        num_layers = st.selectbox(
            "LSTM Katman Sayısı",
            options=[1, 2, 3],
            index=1,
            help="Daha fazla katman = daha derin model"
        )
        
        st.markdown("---")
        st.subheader("🎯 Eğitim Parametreleri")
        
        # Epochs
        epochs = st.slider(
            "Epoch Sayısı",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Eğitim döngü sayısı"
        )
        
        # Batch Size
        batch_size = st.selectbox(
            "Batch Boyutu",
            options=[16, 32, 64, 128],
            index=1
        )
        
        # Learning Rate
        learning_rate = st.select_slider(
            "Öğrenme Oranı",
            options=[0.0001, 0.0005, 0.001, 0.005, 0.01],
            value=0.001
        )
        
        st.markdown("---")
        
        # Eğitim butonu
        train_button = st.button("🚀 Eğitimi Başlat", type="primary")
    
    # Ana içerik
    if train_button:
        run_training(ticker, period, lookback, hidden_size, num_layers, 
                    epochs, batch_size, learning_rate)
    else:
        # Hoş geldin ekranı
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <h3>📊 Veri Toplama</h3>
                    <p>yfinance ile gerçek hisse senedi verileri</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <h3>🧠 LSTM Modeli</h3>
                    <p>Derin öğrenme ile zaman serisi tahmini</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <h3>📈 Görselleştirme</h3>
                    <p>İnteraktif grafikler ve metrikler</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 👈 Soldaki menüden ayarları yapın ve 'Eğitimi Başlat' butonuna tıklayın!")
        
        # Popüler hisseler
        st.markdown("---")
        st.markdown("### 🔥 Popüler Hisseler")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🍎 Apple (AAPL)"):
                st.session_state.ticker = "AAPL"
        with col2:
            if st.button("⚡ Tesla (TSLA)"):
                st.session_state.ticker = "TSLA"
        with col3:
            if st.button("🔍 Google (GOOGL)"):
                st.session_state.ticker = "GOOGL"
        with col4:
            if st.button("🪟 Microsoft (MSFT)"):
                st.session_state.ticker = "MSFT"


def run_training(ticker, period, lookback, hidden_size, num_layers, 
                epochs, batch_size, learning_rate):
    """
    Model eğitimini çalıştır
    """
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1. Veri Toplama
        status_text.text("📥 Veri indiriliyor...")
        progress_bar.progress(10)
        
        df = download_stock_data(ticker=ticker, period=period)
        prices = get_close_prices(df)
        
        st.success(f"✅ {len(prices)} veri noktası indirildi")
        
        # 2. Veri Ön İşleme
        status_text.text("🔄 Veri işleniyor...")
        progress_bar.progress(20)
        
        preprocessor = StockDataPreprocessor(lookback=lookback)
        data_dict = preprocessor.prepare_data(prices)
        
        # 3. Model Oluşturma
        status_text.text("🧠 Model oluşturuluyor...")
        progress_bar.progress(30)
        
        model = LSTMStockPredictor(
            hidden_size=hidden_size,
            num_layers=num_layers
        )
        
        total_params = sum(p.numel() for p in model.parameters())
        st.info(f"🔢 Model parametresi: {total_params:,}")
        
        # 4. Eğitim
        status_text.text(f"🎯 Eğitim yapılıyor ({epochs} epoch)...")
        progress_bar.progress(40)
        
        trainer = StockModelTrainer(model, learning_rate=learning_rate, 
                                   batch_size=batch_size)
        
        # Eğitim progress bar
        epoch_progress = st.progress(0)
        epoch_text = st.empty()
        
        # Basit eğitim (detaylı log olmadan)
        history = trainer.train(
            data_dict['X_train'], data_dict['y_train'],
            data_dict['X_test'], data_dict['y_test'],
            epochs=epochs,
            verbose=False
        )
        
        progress_bar.progress(80)
        
        # 5. Tahmin
        status_text.text("📊 Tahminler yapılıyor...")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        predictions = make_predictions(model, data_dict['X_test'], device=device)
        
        y_test_actual = data_dict['scaler'].inverse_transform(data_dict['y_test'].numpy())
        predictions_actual = data_dict['scaler'].inverse_transform(predictions)
        
        metrics = calculate_metrics(y_test_actual, predictions_actual)
        
        progress_bar.progress(100)
        status_text.text("✅ Tamamlandı!")
        
        # 6. AL/SAT Sinyali
        st.markdown("---")
        st.markdown("## 🎯 AL/SAT SİNYALİ (BUGÜN)")
        
        # En son fiyat ve tahmin
        latest_actual_price = prices[-1]
        latest_prediction = predictions_actual[-1][0]
        
        # Sinyal üret
        signal_generator = TradingSignalGenerator(threshold_percent=2.0)
        latest_signal = signal_generator.get_latest_signal(latest_actual_price, latest_prediction)
        
        # Büyük sinyal kartı
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if latest_signal['action'] == 'AL':
                st.success(f"# {latest_signal['emoji']} {latest_signal['signal']}")
                st.markdown("### 📈 Yükseliş Bekleniyor!")
            elif latest_signal['action'] == 'SAT':
                st.error(f"# {latest_signal['emoji']} {latest_signal['signal']}")
                st.markdown("### 📉 Düşüş Bekleniyor!")
            else:
                st.info(f"# {latest_signal['emoji']} {latest_signal['signal']}")
                st.markdown("### ➡️ Önemli Hareket Yok")
            
            st.markdown(f"### 📅 Bugünün Fiyatı: **${latest_signal['current_price']:.2f}**")
            st.markdown(f"### 🔮 Yarın Tahmini: **${latest_signal['predicted_price']:.2f}**")
            st.markdown(f"### 📊 Beklenen Değişim: **{latest_signal['change_percent']:+.2f}%**")
            st.markdown(f"**💡 Sebep:** {latest_signal['reason']}")
            st.markdown(f"**🎯 Güven Seviyesi:** {latest_signal['confidence']}")
        
        st.markdown("---")
        
        # 7. Sonuç Metrikleri
        st.markdown("---")
        st.markdown("## 📊 Eğitim Sonuçları")
        
        # Metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("RMSE", f"${metrics['RMSE']:.2f}")
        with col2:
            st.metric("MAE", f"${metrics['MAE']:.2f}")
        with col3:
            st.metric("MAPE", f"{metrics['MAPE']:.2f}%")
        with col4:
            st.metric("R² Score", f"{metrics['R2']:.4f}")
        
        # Eğitim grafiği
        st.markdown("### 📉 Eğitim ve Validasyon Kaybı")
        plot_training_loss(history['train_losses'], history['val_losses'])
        
        # Tahmin grafiği
        st.markdown("### 📈 Gerçek vs Tahmin")
        plot_predictions_interactive(y_test_actual.flatten(), 
                                     predictions_actual.flatten(), 
                                     ticker)
        
        # Model kaydet
        model_path = f'{ticker}_model.pth'
        trainer.save_model(model_path)
        st.success(f"💾 Model kaydedildi: {model_path}")
        
    except Exception as e:
        st.error(f"❌ Hata: {str(e)}")
        progress_bar.progress(0)


def plot_training_loss(train_losses, val_losses):
    """
    Eğitim kayıplarını plotla
    """
    fig = go.Figure()
    
    epochs = list(range(1, len(train_losses) + 1))
    
    fig.add_trace(go.Scatter(
        x=epochs,
        y=train_losses,
        mode='lines',
        name='Eğitim Kaybı',
        line=dict(color='#007acc', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=epochs,
        y=val_losses,
        mode='lines',
        name='Validasyon Kaybı',
        line=dict(color='#f44336', width=2)
    ))
    
    fig.update_layout(
        title="Model Eğitim Geçmişi",
        xaxis_title="Epoch",
        yaxis_title="Kayıp (MSE)",
        hovermode='x unified',
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_predictions_interactive(y_true, y_pred, ticker):
    """
    Tahminleri interaktif plotla
    """
    fig = go.Figure()
    
    test_indices = list(range(len(y_true)))
    
    fig.add_trace(go.Scatter(
        x=test_indices,
        y=y_true,
        mode='lines',
        name='Gerçek Fiyat',
        line=dict(color='#4CAF50', width=2),
        hovertemplate='Gerçek: $%{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=test_indices,
        y=y_pred,
        mode='lines',
        name='Tahmin',
        line=dict(color='#FF9800', width=2, dash='dash'),
        hovertemplate='Tahmin: $%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{ticker} Hisse Senedi Fiyat Tahmini",
        xaxis_title="Test Veri Noktası",
        yaxis_title="Fiyat ($)",
        hovermode='x unified',
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
