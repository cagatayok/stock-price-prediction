"""
Tahmin yapma ve görselleştirme modülü
"""
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


def make_predictions(model, X_test, device='cpu'):
    """
    Test verisi üzerinde tahminler yap
    
    Args:
        model (nn.Module): Eğitilmiş model
        X_test (torch.Tensor): Test girdileri
        device (str): Hesaplama cihazı
    
    Returns:
        np.array: Tahminler
    """
    model.eval()
    model.to(device)
    X_test = X_test.to(device)
    
    with torch.no_grad():
        predictions = model(X_test)
    
    return predictions.cpu().numpy()


def calculate_metrics(y_true, y_pred):
    """
    Tahmin performans metriklerini hesapla
    
    Args:
        y_true (np.array): Gerçek değerler
        y_pred (np.array): Tahmin edilen değerler
    
    Returns:
        dict: Metrikler
    """
    # Mean Absolute Error (MAE)
    mae = np.mean(np.abs(y_true - y_pred))
    
    # Mean Squared Error (MSE)
    mse = np.mean((y_true - y_pred) ** 2)
    
    # Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    
    # Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    # R² Score
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }


def print_metrics(metrics):
    """
    Metrikleri yazdır
    
    Args:
        metrics (dict): Performans metrikleri
    """
    print(f"\n{'='*60}")
    print(f"TAHMIN PERFORMANSI")
    print(f"{'='*60}")
    print(f"📊 MAE (Mean Absolute Error):      ${metrics['MAE']:.2f}")
    print(f"📊 RMSE (Root Mean Squared Error): ${metrics['RMSE']:.2f}")
    print(f"📊 MAPE (Mean Absolute % Error):   {metrics['MAPE']:.2f}%")
    print(f"📊 R² Score:                        {metrics['R2']:.4f}")
    print(f"{'='*60}\n")


def plot_training_history(train_losses, val_losses, save_path='training_history.png'):
    """
    Eğitim ve validasyon kayıp grafiği çiz
    
    Args:
        train_losses (list): Eğitim kayıpları
        val_losses (list): Validasyon kayıpları
        save_path (str): Grafik kayıt yolu
    """
    plt.figure(figsize=(12, 6))
    
    epochs = range(1, len(train_losses) + 1)
    
    plt.plot(epochs, train_losses, 'b-', label='Eğitim Kaybı', linewidth=2)
    plt.plot(epochs, val_losses, 'r-', label='Validasyon Kaybı', linewidth=2)
    
    plt.title('Model Eğitim Geçmişi', fontsize=16, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Kayıp (MSE)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"📊 Eğitim grafiği kaydedildi: {save_path}")
    plt.close()


def plot_predictions(y_true, y_pred, ticker='Stock', lookback=60, 
                    train_size=None, save_path='predictions.png'):
    """
    Gerçek ve tahmin edilen fiyatları çiz
    
    Args:
        y_true (np.array): Gerçek fiyatlar
        y_pred (np.array): Tahmin edilen fiyatlar
        ticker (str): Hisse sembolü
        lookback (int): Geçmişe bakış penceresi
        train_size (int): Eğitim veri sayısı
        save_path (str): Grafik kayıt yolu
    """
    plt.figure(figsize=(16, 8))
    
    # X ekseni (gün indeksleri)
    test_indices = range(len(y_true))
    
    # Gerçek değerler
    plt.plot(test_indices, y_true, 'b-', label='Gerçek Fiyat', 
             linewidth=2, alpha=0.7)
    
    # Tahminler
    plt.plot(test_indices, y_pred, 'r--', label='Tahmin Edilen Fiyat', 
             linewidth=2, alpha=0.8)
    
    # Eğitim/test ayrım çizgisi (varsa)
    if train_size:
        plt.axvline(x=0, color='green', linestyle=':', linewidth=2, 
                   label='Test Başlangıcı', alpha=0.7)
    
    plt.title(f'{ticker} Hisse Senedi Fiyat Tahmini', 
              fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Test Veri Noktası', fontsize=14)
    plt.ylabel('Fiyat ($)', fontsize=14)
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    
    # Metrikleri grafiğe ekle
    metrics = calculate_metrics(y_true, y_pred)
    textstr = f"RMSE: ${metrics['RMSE']:.2f}\n"
    textstr += f"MAE: ${metrics['MAE']:.2f}\n"
    textstr += f"MAPE: {metrics['MAPE']:.2f}%\n"
    textstr += f"R²: {metrics['R2']:.4f}"
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, 
             fontsize=11, verticalalignment='top', bbox=props, 
             family='monospace')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"📊 Tahmin grafiği kaydedildi: {save_path}")
    plt.close()


def plot_predictions_zoomed(y_true, y_pred, ticker='Stock', 
                           zoom_start=0, zoom_length=100, 
                           save_path='predictions_zoomed.png'):
    """
    Yakınlaştırılmış tahmin grafiği (daha detaylı görünüm)
    
    Args:
        y_true (np.array): Gerçek fiyatlar
        y_pred (np.array): Tahmin edilen fiyatlar
        ticker (str): Hisse sembolü
        zoom_start (int): Zoom başlangıcı
        zoom_length (int): Zoom uzunluğu
        save_path (str): Grafik kayıt yolu
    """
    zoom_end = min(zoom_start + zoom_length, len(y_true))
    
    plt.figure(figsize=(16, 8))
    
    indices = range(zoom_start, zoom_end)
    y_true_zoom = y_true[zoom_start:zoom_end]
    y_pred_zoom = y_pred[zoom_start:zoom_end]
    
    plt.plot(indices, y_true_zoom, 'bo-', label='Gerçek Fiyat', 
             linewidth=2, markersize=6, alpha=0.7)
    plt.plot(indices, y_pred_zoom, 'r^--', label='Tahmin', 
             linewidth=2, markersize=6, alpha=0.8)
    
    plt.title(f'{ticker} - Detaylı Görünüm (İlk {zoom_length} Test Örneği)', 
              fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Test Veri Noktası', fontsize=14)
    plt.ylabel('Fiyat ($)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"📊 Yakınlaştırılmış grafik kaydedildi: {save_path}")
    plt.close()


if __name__ == "__main__":
    # Test
    print("🧪 Prediction modülü testi...\n")
    
    # Sahte veri
    y_true = np.random.randn(200) * 10 + 150
    y_pred = y_true + np.random.randn(200) * 5  # Biraz gürültü ekle
    
    # Metrikler
    metrics = calculate_metrics(y_true, y_pred)
    print_metrics(metrics)
    
    # Grafikler
    plot_predictions(y_true, y_pred, ticker='TEST', save_path='test_predictions.png')
    plot_predictions_zoomed(y_true, y_pred, ticker='TEST', 
                           zoom_length=50, save_path='test_zoomed.png')
    
    print("✅ Test tamamlandı!")
