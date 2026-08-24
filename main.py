"""
Ana uygulama - Tüm adımları birleştiren script
"""
import argparse
import torch
import numpy as np
from data_collection import download_stock_data, get_close_prices
from data_preprocessing import StockDataPreprocessor
from model import LSTMStockPredictor, print_model_summary
from train import StockModelTrainer
from predict import (make_predictions, calculate_metrics, print_metrics,
                     plot_training_history, plot_predictions, plot_predictions_zoomed)
from trading_signals import TradingSignalGenerator, print_latest_signal, print_signal_summary


def main(ticker='AAPL', period='5y', lookback=60, hidden_size=64, 
         num_layers=2, epochs=100, batch_size=32, learning_rate=0.001):
    """
    Hisse senedi fiyat tahmin pipeline'ı
    
    Args:
        ticker (str): Hisse senedi sembolü
        period (str): Veri çekme periyodu
        lookback (int): Geçmişe bakış penceresi (gün)
        hidden_size (int): LSTM gizli katman boyutu
        num_layers (int): LSTM katman sayısı
        epochs (int): Eğitim epoch sayısı
        batch_size (int): Batch boyutu
        learning_rate (float): Öğrenme oranı
    """
    
    print(f"\n{'#'*60}")
    print(f"#  HİSSE SENEDİ FİYAT TAHMİN SİSTEMİ - PyTorch LSTM")
    print(f"{'#'*60}")
    print(f"#  Hisse: {ticker}")
    print(f"#  Periyot: {period}")
    print(f"#  Model: {num_layers}-katmanlı LSTM (hidden_size={hidden_size})")
    print(f"#  Eğitim: {epochs} epoch, batch_size={batch_size}")
    print(f"{'#'*60}\n")
    
    # ========== 1. VERİ TOPLAMA ==========
    print(f"{'='*60}")
    print(f"ADIM 1: VERİ TOPLAMA")
    print(f"{'='*60}\n")
    
    df = download_stock_data(ticker=ticker, period=period, interval='1d')
    prices = get_close_prices(df)
    
    # ========== 2. VERİ ÖN İŞLEME ==========
    preprocessor = StockDataPreprocessor(lookback=lookback, train_split=0.8)
    data_dict = preprocessor.prepare_data(prices)
    
    X_train = data_dict['X_train']
    y_train = data_dict['y_train']
    X_test = data_dict['X_test']
    y_test = data_dict['y_test']
    scaler = data_dict['scaler']
    
    # ========== 3. MODEL OLUŞTURMA ==========
    print(f"{'='*60}")
    print(f"ADIM 3: MODEL OLUŞTURMA")
    print(f"{'='*60}\n")
    
    model = LSTMStockPredictor(
        input_size=1,
        hidden_size=hidden_size,
        num_layers=num_layers,
        output_size=1,
        dropout=0.2
    )
    
    print_model_summary(model, input_size=(batch_size, lookback, 1))
    
    # ========== 4. MODEL EĞİTİMİ ==========
    trainer = StockModelTrainer(model, learning_rate=learning_rate, batch_size=batch_size)
    
    history = trainer.train(
        X_train, y_train, 
        X_test, y_test,  # Test veriyi validasyon olarak kullanıyoruz
        epochs=epochs, 
        verbose=True
    )
    
    # Eğitim grafiği
    plot_training_history(
        history['train_losses'], 
        history['val_losses'],
        save_path=f'{ticker}_training_history.png'
    )
    
    # Modeli kaydet
    trainer.save_model(filepath=f'{ticker}_model.pth')
    
    # ========== 5. TAHMİN VE DEĞERLENDİRME ==========
    print(f"{'='*60}")
    print(f"ADIM 5: TAHMİN VE DEĞERLENDİRME")
    print(f"{'='*60}\n")
    
    # Test verisi üzerinde tahmin yap
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    predictions = make_predictions(model, X_test, device=device)
    
    # Ölçeklendirilmiş değerleri orijinal ölçeğe geri çevir
    y_test_actual = scaler.inverse_transform(y_test.numpy())
    predictions_actual = scaler.inverse_transform(predictions)
    
    # Performans metrikleri
    metrics = calculate_metrics(y_test_actual, predictions_actual)
    print_metrics(metrics)
    
    # Tahmin grafikleri
    plot_predictions(
        y_test_actual.flatten(), 
        predictions_actual.flatten(),
        ticker=ticker,
        lookback=lookback,
        train_size=len(X_train),
        save_path=f'{ticker}_predictions.png'
    )
    
    plot_predictions_zoomed(
        y_test_actual.flatten(),
        predictions_actual.flatten(),
        ticker=ticker,
        zoom_length=min(100, len(y_test)),
        save_path=f'{ticker}_predictions_zoomed.png'
    )
    
    # ========== AL/SAT SİNYALLERİ ==========
    print(f"{'='*60}")
    print(f"ADIM 6: AL/SAT SİNYALLERİ")
    print(f"{'='*60}\n")
    
    # Sinyal üreteci
    signal_generator = TradingSignalGenerator(threshold_percent=2.0)
    
    # Test verisi için sinyaller
    test_signals, test_percentages = signal_generator.generate_signals(
        y_test_actual[:-1].flatten(),  # Bugünkü fiyatlar
        y_test_actual[1:].flatten()    # Yarınki gerçek fiyatlar (karşılaştırma için)
    )
    
    # Tahminler için sinyaller
    pred_signals, pred_percentages = signal_generator.generate_signals(
        y_test_actual[:-1].flatten(),      # Bugünkü fiyatlar
        predictions_actual[:-1].flatten()  # Yarınki tahminler
    )
    
    # Özet
    print_signal_summary(pred_signals, ticker)
    
    # EN ÖNEMLİ: Son günün sinyali (BUGÜN NE YAPMALIYIZ?)
    latest_actual_price = prices[-1]  # En son gerçek fiyat
    latest_prediction = predictions_actual[-1][0]  # En son tahmin
    
    latest_signal = print_latest_signal(
        ticker, 
        latest_actual_price, 
        latest_prediction,
        threshold=2.0
    )
    
    # ========== ÖZET ==========
    print(f"\n{'#'*60}")
    print(f"#  PROJE TAMAMLANDI! ✅")
    print(f"{'#'*60}")
    print(f"#  📊 Model performansı:")
    print(f"#     - RMSE: ${metrics['RMSE']:.2f}")
    print(f"#     - MAE: ${metrics['MAE']:.2f}")
    print(f"#     - MAPE: {metrics['MAPE']:.2f}%")
    print(f"#     - R² Score: {metrics['R2']:.4f}")
    print(f"#")
    print(f"#  🎯 AL/SAT Sinyali (BUGÜN):")
    print(f"#     {latest_signal['emoji']} {latest_signal['action']}")
    print(f"#     Bugün: ${latest_signal['current_price']:.2f}")
    print(f"#     Yarın Tahmini: ${latest_signal['predicted_price']:.2f}")
    print(f"#     Değişim: {latest_signal['change_percent']:+.2f}%")
    print(f"#     {latest_signal['reason']}")
    print(f"#")
    print(f"#  💾 Kaydedilen dosyalar:")
    print(f"#     - {ticker}_model.pth (Eğitilmiş model)")
    print(f"#     - {ticker}_training_history.png (Eğitim grafiği)")
    print(f"#     - {ticker}_predictions.png (Tahmin grafiği)")
    print(f"#     - {ticker}_predictions_zoomed.png (Detaylı görünüm)")
    print(f"{'#'*60}\n")
    
    return model, metrics, history, latest_signal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hisse Senedi Fiyat Tahmini - PyTorch LSTM')
    
    parser.add_argument('--ticker', type=str, default='AAPL',
                       help='Hisse senedi sembolü (örn: AAPL, TSLA, GOOGL)')
    parser.add_argument('--period', type=str, default='5y',
                       help='Veri periyodu (örn: 1y, 5y, 10y)')
    parser.add_argument('--lookback', type=int, default=60,
                       help='Geçmişe bakış penceresi (gün)')
    parser.add_argument('--hidden-size', type=int, default=64,
                       help='LSTM gizli katman boyutu')
    parser.add_argument('--num-layers', type=int, default=2,
                       help='LSTM katman sayısı')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Eğitim epoch sayısı')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch boyutu')
    parser.add_argument('--learning-rate', type=float, default=0.001,
                       help='Öğrenme oranı')
    
    args = parser.parse_args()
    
    # Ana fonksiyonu çalıştır
    model, metrics, history, signal = main(
        ticker=args.ticker,
        period=args.period,
        lookback=args.lookback,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate
    )
