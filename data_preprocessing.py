"""
Veri ön işleme ve zaman penceresi oluşturma modülü
"""
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler


class StockDataPreprocessor:
    """
    Hisse senedi verilerini PyTorch LSTM için hazırlar
    """
    
    def __init__(self, lookback=60, train_split=0.8):
        """
        Args:
            lookback (int): Geçmişe bakış penceresi (örn: 60 gün)
            train_split (float): Eğitim verisi oranı (0-1 arası)
        """
        self.lookback = lookback
        self.train_split = train_split
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = None
        self.original_data = None
        
    def fit_transform(self, data):
        """
        Veriyi ölçeklendir (0-1 arası)
        
        Args:
            data (np.array): Ham fiyat verileri (1D array)
        
        Returns:
            np.array: Ölçeklendirilmiş veri
        """
        self.original_data = data
        
        # Veriyi 2D array'e çevir (sklearn için gerekli)
        data_reshaped = data.reshape(-1, 1)
        
        # 0-1 arası ölçeklendir
        self.scaled_data = self.scaler.fit_transform(data_reshaped)
        
        print(f"🔄 Veri ölçeklendirildi:")
        print(f"   Orjinal aralık: [{data.min():.2f}, {data.max():.2f}]")
        print(f"   Ölçekli aralık: [{self.scaled_data.min():.4f}, {self.scaled_data.max():.4f}]")
        
        return self.scaled_data
    
    def inverse_transform(self, scaled_data):
        """
        Ölçeklendirilmiş veriyi orijinal aralığa geri çevir
        
        Args:
            scaled_data (np.array or torch.Tensor): Ölçeklendirilmiş veri
        
        Returns:
            np.array: Orijinal ölçekteki veri
        """
        if isinstance(scaled_data, torch.Tensor):
            scaled_data = scaled_data.cpu().numpy()
        
        return self.scaler.inverse_transform(scaled_data)
    
    def create_sequences(self, data):
        """
        Zaman pencereli (sliding window) sekanslar oluştur
        
        Örnek: lookback=60 için
        X[0] = [gün_0, gün_1, ..., gün_59]
        y[0] = gün_60
        
        Args:
            data (np.array): Ölçeklendirilmiş veri
        
        Returns:
            tuple: (X, y) - Girdi sekansları ve hedef değerler
        """
        X, y = [], []
        
        for i in range(self.lookback, len(data)):
            # Son 'lookback' gün
            X.append(data[i-self.lookback:i, 0])
            # Tahmin edilecek gün
            y.append(data[i, 0])
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"🪟 Zaman pencereleri oluşturuldu:")
        print(f"   Pencere boyutu: {self.lookback} gün")
        print(f"   Toplam örnek sayısı: {len(X)}")
        print(f"   X shape: {X.shape}, y shape: {y.shape}")
        
        return X, y
    
    def train_test_split(self, X, y):
        """
        Veriyi eğitim ve test setlerine ayır
        
        Args:
            X (np.array): Girdi sekansları
            y (np.array): Hedef değerler
        
        Returns:
            tuple: (X_train, y_train, X_test, y_test)
        """
        split_idx = int(len(X) * self.train_split)
        
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"✂️  Veri bölündü:")
        print(f"   Eğitim: {len(X_train)} örnek ({self.train_split*100:.0f}%)")
        print(f"   Test: {len(X_test)} örnek ({(1-self.train_split)*100:.0f}%)")
        
        return X_train, y_train, X_test, y_test
    
    def to_pytorch_tensors(self, X, y):
        """
        NumPy array'leri PyTorch tensorlerine çevir
        
        Args:
            X (np.array): Girdi sekansları
            y (np.array): Hedef değerler
        
        Returns:
            tuple: (X_tensor, y_tensor)
        """
        # LSTM için shape: (batch_size, sequence_length, num_features)
        X_tensor = torch.FloatTensor(X).unsqueeze(-1)  # (N, lookback, 1)
        y_tensor = torch.FloatTensor(y).unsqueeze(-1)  # (N, 1)
        
        print(f"🔥 PyTorch tensorlere dönüştürüldü:")
        print(f"   X shape: {X_tensor.shape} (batch, sequence, features)")
        print(f"   y shape: {y_tensor.shape}")
        
        return X_tensor, y_tensor
    
    def prepare_data(self, data):
        """
        Tüm ön işleme adımlarını birleştir
        
        Args:
            data (np.array): Ham fiyat verileri
        
        Returns:
            dict: Hazırlanmış veri setleri
        """
        print(f"\n{'='*60}")
        print(f"VERİ ÖN İŞLEME BAŞLIYOR")
        print(f"{'='*60}\n")
        
        # 1. Ölçeklendirme
        scaled_data = self.fit_transform(data)
        
        # 2. Zaman pencereleri oluştur
        X, y = self.create_sequences(scaled_data)
        
        # 3. Eğitim/test ayırma
        X_train, y_train, X_test, y_test = self.train_test_split(X, y)
        
        # 4. PyTorch tensorlerine çevir
        X_train_tensor, y_train_tensor = self.to_pytorch_tensors(X_train, y_train)
        X_test_tensor, y_test_tensor = self.to_pytorch_tensors(X_test, y_test)
        
        print(f"\n{'='*60}")
        print(f"VERİ ÖN İŞLEME TAMAMLANDI ✅")
        print(f"{'='*60}\n")
        
        return {
            'X_train': X_train_tensor,
            'y_train': y_train_tensor,
            'X_test': X_test_tensor,
            'y_test': y_test_tensor,
            'scaler': self.scaler
        }


if __name__ == "__main__":
    # Test
    test_data = np.random.randn(1000) * 10 + 100  # Sahte hisse senedi verileri
    
    preprocessor = StockDataPreprocessor(lookback=60, train_split=0.8)
    data_dict = preprocessor.prepare_data(test_data)
    
    print("\nHazır veriler:")
    for key, value in data_dict.items():
        if isinstance(value, torch.Tensor):
            print(f"{key}: {value.shape}")
