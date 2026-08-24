"""
Model eğitim modülü
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import time


class StockModelTrainer:
    """
    LSTM modelini eğiten sınıf
    """
    
    def __init__(self, model, learning_rate=0.001, batch_size=32):
        """
        Args:
            model (nn.Module): Eğitilecek PyTorch modeli
            learning_rate (float): Öğrenme oranı
            batch_size (int): Batch boyutu
        """
        self.model = model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        
        # GPU varsa kullan
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Kayıp fonksiyonu (MSE - Mean Squared Error)
        self.criterion = nn.MSELoss()
        
        # Optimizer (Adam)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Eğitim geçmişi
        self.train_losses = []
        self.val_losses = []
        
        print(f"🎯 Trainer hazır:")
        print(f"   Cihaz: {self.device}")
        print(f"   Öğrenme oranı: {learning_rate}")
        print(f"   Batch boyutu: {batch_size}")
        print(f"   Kayıp fonksiyonu: MSE (Mean Squared Error)")
        print(f"   Optimizer: Adam")
    
    def create_data_loader(self, X, y, shuffle=True):
        """
        PyTorch DataLoader oluştur
        
        Args:
            X (torch.Tensor): Girdi verileri
            y (torch.Tensor): Hedef değerler
            shuffle (bool): Veriyi karıştır
        
        Returns:
            DataLoader: PyTorch veri yükleyici
        """
        dataset = TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=shuffle)
        return loader
    
    def train_epoch(self, train_loader):
        """
        Bir epoch eğitim yap
        
        Args:
            train_loader (DataLoader): Eğitim verisi
        
        Returns:
            float: Ortalama kayıp
        """
        self.model.train()
        epoch_loss = 0.0
        
        for batch_X, batch_y in train_loader:
            # Veriyi cihaza taşı
            batch_X = batch_X.to(self.device)
            batch_y = batch_y.to(self.device)
            
            # Gradyanları sıfırla
            self.optimizer.zero_grad()
            
            # İleri yayılım
            predictions = self.model(batch_X)
            
            # Kayıp hesapla
            loss = self.criterion(predictions, batch_y)
            
            # Geri yayılım
            loss.backward()
            
            # Ağırlıkları güncelle
            self.optimizer.step()
            
            epoch_loss += loss.item()
        
        # Ortalama kayıp
        avg_loss = epoch_loss / len(train_loader)
        return avg_loss
    
    def validate(self, val_loader):
        """
        Validasyon yap
        
        Args:
            val_loader (DataLoader): Validasyon verisi
        
        Returns:
            float: Ortalama kayıp
        """
        self.model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X = batch_X.to(self.device)
                batch_y = batch_y.to(self.device)
                
                predictions = self.model(batch_X)
                loss = self.criterion(predictions, batch_y)
                val_loss += loss.item()
        
        avg_loss = val_loss / len(val_loader)
        return avg_loss
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, verbose=True):
        """
        Modeli eğit
        
        Args:
            X_train (torch.Tensor): Eğitim girdileri
            y_train (torch.Tensor): Eğitim hedefleri
            X_val (torch.Tensor): Validasyon girdileri
            y_val (torch.Tensor): Validasyon hedefleri
            epochs (int): Epoch sayısı
            verbose (bool): İlerleme mesajlarını göster
        
        Returns:
            dict: Eğitim geçmişi
        """
        print(f"\n{'='*60}")
        print(f"MODEL EĞİTİMİ BAŞLIYOR")
        print(f"{'='*60}\n")
        print(f"📈 Epoch sayısı: {epochs}")
        
        # DataLoader'ları oluştur
        train_loader = self.create_data_loader(X_train, y_train, shuffle=True)
        val_loader = self.create_data_loader(X_val, y_val, shuffle=False)
        
        print(f"   Eğitim batch sayısı: {len(train_loader)}")
        print(f"   Validasyon batch sayısı: {len(val_loader)}\n")
        
        start_time = time.time()
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            # Eğitim
            train_loss = self.train_epoch(train_loader)
            self.train_losses.append(train_loss)
            
            # Validasyon
            val_loss = self.validate(val_loader)
            self.val_losses.append(val_loss)
            
            # En iyi model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epoch + 1
            
            # İlerleme mesajı
            if verbose and (epoch + 1) % 10 == 0:
                elapsed = time.time() - start_time
                print(f"Epoch [{epoch+1:3d}/{epochs}] | "
                      f"Train Loss: {train_loss:.6f} | "
                      f"Val Loss: {val_loss:.6f} | "
                      f"Süre: {elapsed:.1f}s")
        
        total_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"EĞİTİM TAMAMLANDI ✅")
        print(f"{'='*60}")
        print(f"⏱️  Toplam süre: {total_time:.1f} saniye")
        print(f"🏆 En iyi validasyon kaybı: {best_val_loss:.6f} (Epoch {best_epoch})")
        print(f"📉 Son eğitim kaybı: {self.train_losses[-1]:.6f}")
        print(f"📉 Son validasyon kaybı: {self.val_losses[-1]:.6f}")
        print(f"{'='*60}\n")
        
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'best_val_loss': best_val_loss,
            'best_epoch': best_epoch,
            'total_time': total_time
        }
    
    def save_model(self, filepath='stock_model.pth'):
        """
        Modeli kaydet
        
        Args:
            filepath (str): Kayıt yolu
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'train_losses': self.train_losses,
            'val_losses': self.val_losses
        }, filepath)
        print(f"💾 Model kaydedildi: {filepath}")
    
    def load_model(self, filepath='stock_model.pth'):
        """
        Modeli yükle
        
        Args:
            filepath (str): Model dosya yolu
        """
        checkpoint = torch.load(filepath)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.train_losses = checkpoint['train_losses']
        self.val_losses = checkpoint['val_losses']
        print(f"📂 Model yüklendi: {filepath}")


if __name__ == "__main__":
    # Test
    from model import LSTMStockPredictor
    
    print("🧪 Trainer testi yapılıyor...\n")
    
    # Sahte veri oluştur
    X_train = torch.randn(800, 60, 1)
    y_train = torch.randn(800, 1)
    X_val = torch.randn(200, 60, 1)
    y_val = torch.randn(200, 1)
    
    # Model oluştur
    model = LSTMStockPredictor(hidden_size=32, num_layers=1)
    
    # Trainer oluştur
    trainer = StockModelTrainer(model, learning_rate=0.001, batch_size=32)
    
    # Eğit (kısa test)
    history = trainer.train(X_train, y_train, X_val, y_val, epochs=5, verbose=True)
    
    print("\n✅ Trainer testi başarılı!")
