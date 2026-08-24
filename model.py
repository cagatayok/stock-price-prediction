"""
LSTM tabanlı hisse senedi fiyat tahmin modeli
"""
import torch
import torch.nn as nn


class LSTMStockPredictor(nn.Module):
    """
    LSTM (Long Short-Term Memory) sinir ağı ile hisse senedi fiyat tahmini
    
    LSTM, geçmiş verilerdeki uzun vadeli bağımlılıkları öğrenebilen 
    özel bir tekrarlayan sinir ağı (RNN) türüdür.
    """
    
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1, dropout=0.2):
        """
        Args:
            input_size (int): Girdi özellik sayısı (fiyat için 1)
            hidden_size (int): LSTM gizli katman boyutu
            num_layers (int): LSTM katman sayısı
            output_size (int): Çıktı boyutu (bir sonraki günün fiyatı için 1)
            dropout (float): Dropout oranı (overfitting'i önlemek için)
        """
        super(LSTMStockPredictor, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM katmanları
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,  # (batch, seq, feature) formatı
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Tam bağlantılı katman (LSTM çıktısını nihai tahmine dönüştürür)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        """
        İleri yayılım (forward pass)
        
        Args:
            x (torch.Tensor): Girdi tensoru, shape: (batch_size, sequence_length, input_size)
        
        Returns:
            torch.Tensor: Tahmin edilen fiyat, shape: (batch_size, output_size)
        """
        # LSTM ilk hidden ve cell state'leri (sıfırlarla başla)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # LSTM'den geçir
        # out: (batch, seq_len, hidden_size)
        # hn, cn: Son hidden ve cell state'ler
        out, (hn, cn) = self.lstm(x, (h0, c0))
        
        # Sadece son zaman adımının çıktısını kullan
        out = out[:, -1, :]  # (batch, hidden_size)
        
        # Tam bağlantılı katmandan geçir
        out = self.fc(out)  # (batch, output_size)
        
        return out
    
    def predict(self, x):
        """
        Tahmin modu (evaluation mode)
        
        Args:
            x (torch.Tensor): Girdi tensoru
        
        Returns:
            torch.Tensor: Tahminler
        """
        self.eval()  # Evaluation mode (dropout kapalı)
        with torch.no_grad():
            predictions = self.forward(x)
        return predictions


def count_parameters(model):
    """
    Modeldeki eğitilebilir parametre sayısını hesapla
    
    Args:
        model (nn.Module): PyTorch modeli
    
    Returns:
        int: Toplam parametre sayısı
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def print_model_summary(model, input_size=(1, 60, 1)):
    """
    Model mimarisinin özetini yazdır
    
    Args:
        model (nn.Module): PyTorch modeli
        input_size (tuple): Örnek girdi boyutu (batch, seq_len, features)
    """
    print(f"\n{'='*60}")
    print(f"MODEL MİMARİSİ")
    print(f"{'='*60}\n")
    
    print(model)
    
    print(f"\n📊 Model İstatistikleri:")
    print(f"   Toplam parametre sayısı: {count_parameters(model):,}")
    
    # Test girdi
    test_input = torch.randn(*input_size)
    test_output = model(test_input)
    
    print(f"   Girdi shape: {test_input.shape}")
    print(f"   Çıktı shape: {test_output.shape}")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # Test
    print("🧪 Model testi yapılıyor...\n")
    
    # Küçük bir model oluştur
    model = LSTMStockPredictor(
        input_size=1,
        hidden_size=64,
        num_layers=2,
        output_size=1,
        dropout=0.2
    )
    
    # Model özetini yazdır
    print_model_summary(model, input_size=(32, 60, 1))
    
    # Örnek tahmin
    test_data = torch.randn(32, 60, 1)  # 32 örnek, 60 gün, 1 özellik
    predictions = model.predict(test_data)
    
    print(f"✅ Test tahmini başarılı!")
    print(f"   Tahmin shape: {predictions.shape}")
    print(f"   İlk 5 tahmin: {predictions[:5].squeeze().tolist()}")
