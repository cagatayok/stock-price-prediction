"""
Hisse Senedi Fiyat Tahmini - Grafiksel Arayüz (GUI)
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import torch
from datetime import datetime
import os
from data_collection import download_stock_data, get_close_prices
from data_preprocessing import StockDataPreprocessor
from model import LSTMStockPredictor
from train import StockModelTrainer
from predict import (make_predictions, calculate_metrics, print_metrics,
                     plot_training_history, plot_predictions, plot_predictions_zoomed)


class StockPredictionApp:
    """
    Hisse senedi tahmin uygulaması GUI
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Hisse Senedi Fiyat Tahmini - PyTorch LSTM")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Tema renkleri
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.success_color = "#4CAF50"
        self.error_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        # Eğitim durumu
        self.is_training = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        GUI bileşenlerini oluştur
        """
        # ============ BAŞLIK ============
        title_frame = tk.Frame(self.root, bg=self.accent_color)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="📈 Hisse Senedi Fiyat Tahmini - PyTorch LSTM",
            font=("Arial", 18, "bold"),
            bg=self.accent_color,
            fg="white",
            pady=15
        )
        title_label.pack()
        
        # ============ ANA KONTEYNER ============
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sol panel - Ayarlar
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Sağ panel - Log
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ============ AYARLAR PANELİ ============
        settings_label = tk.Label(
            left_frame,
            text="⚙️ Model Ayarları",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        settings_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Hisse Sembolü
        self.create_input_field(left_frame, "Hisse Sembolü:", "AAPL", "ticker_entry")
        
        # Periyot
        self.create_dropdown_field(left_frame, "Veri Periyodu:", 
                                   ["1y", "2y", "3y", "5y", "10y"], "5y", "period_var")
        
        # Lookback
        self.create_input_field(left_frame, "Geçmiş Pencere (gün):", "60", "lookback_entry")
        
        # Hidden Size
        self.create_dropdown_field(left_frame, "LSTM Boyutu:", 
                                   ["32", "64", "128", "256"], "64", "hidden_size_var")
        
        # Num Layers
        self.create_dropdown_field(left_frame, "LSTM Katman Sayısı:", 
                                   ["1", "2", "3"], "2", "num_layers_var")
        
        # Epochs
        self.create_input_field(left_frame, "Epoch Sayısı:", "50", "epochs_entry")
        
        # Batch Size
        self.create_dropdown_field(left_frame, "Batch Boyutu:", 
                                   ["16", "32", "64", "128"], "32", "batch_size_var")
        
        # Learning Rate
        self.create_input_field(left_frame, "Öğrenme Oranı:", "0.001", "lr_entry")
        
        # ============ BUTONLAR ============
        button_frame = tk.Frame(left_frame, bg=self.bg_color)
        button_frame.pack(pady=20, fill=tk.X)
        
        self.train_button = tk.Button(
            button_frame,
            text="🚀 Eğitimi Başlat",
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="white",
            command=self.start_training,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.train_button.pack(fill=tk.X, pady=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="⛔ Durdur",
            font=("Arial", 12, "bold"),
            bg=self.error_color,
            fg="white",
            command=self.stop_training,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(fill=tk.X, pady=(0, 10))
        
        self.open_results_button = tk.Button(
            button_frame,
            text="📊 Sonuçları Aç",
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.open_results,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.open_results_button.pack(fill=tk.X)
        
        # ============ LOG PANELİ ============
        log_label = tk.Label(
            right_frame,
            text="📝 Eğitim Logları",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        log_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            right_frame,
            width=50,
            height=30,
            font=("Consolas", 9),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="white",
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # ============ DURUM ÇUBUĞU ============
        self.status_frame = tk.Frame(self.root, bg="#2d2d2d", height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="✅ Hazır",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg=self.success_color,
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            mode='indeterminate',
            length=200
        )
        
        # Hoş geldin mesajı
        self.log("🎯 Hisse Senedi Fiyat Tahmin Sistemi Hazır!", "success")
        self.log("💡 Ayarları yapın ve 'Eğitimi Başlat' butonuna tıklayın.", "info")
        self.log("⚠️ Not: yfinance geçmiş verileri çeker (günlük kapanış fiyatları)", "warning")
    
    def create_input_field(self, parent, label_text, default_value, var_name):
        """
        Giriş alanı oluştur
        """
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=label_text, font=("Arial", 10), 
                        bg=self.bg_color, fg=self.fg_color, width=20, anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(frame, font=("Arial", 10), width=15)
        entry.insert(0, default_value)
        entry.pack(side=tk.RIGHT)
        
        setattr(self, var_name, entry)
    
    def create_dropdown_field(self, parent, label_text, options, default_value, var_name):
        """
        Dropdown menü oluştur
        """
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=label_text, font=("Arial", 10), 
                        bg=self.bg_color, fg=self.fg_color, width=20, anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        var = tk.StringVar(value=default_value)
        dropdown = ttk.Combobox(frame, textvariable=var, values=options, 
                               font=("Arial", 10), width=13, state="readonly")
        dropdown.pack(side=tk.RIGHT)
        
        setattr(self, var_name, var)
    
    def log(self, message, level="info"):
        """
        Log mesajı ekle
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "info": "#ffffff",
            "success": "#4CAF50",
            "warning": "#FFC107",
            "error": "#f44336"
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status(self, text, color):
        """
        Durum çubuğunu güncelle
        """
        self.status_label.config(text=text, fg=color)
    
    def get_parameters(self):
        """
        Kullanıcı parametrelerini al
        """
        try:
            params = {
                'ticker': self.ticker_entry.get().upper().strip(),
                'period': self.period_var.get(),
                'lookback': int(self.lookback_entry.get()),
                'hidden_size': int(self.hidden_size_var.get()),
                'num_layers': int(self.num_layers_var.get()),
                'epochs': int(self.epochs_entry.get()),
                'batch_size': int(self.batch_size_var.get()),
                'learning_rate': float(self.lr_entry.get())
            }
            return params
        except ValueError as e:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin!")
            return None
    
    def start_training(self):
        """
        Eğitimi başlat
        """
        params = self.get_parameters()
        if not params:
            return
        
        # Durum güncelle
        self.is_training = True
        self.train_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_status("🔄 Eğitim devam ediyor...", "#FFC107")
        self.progress_bar.pack(side=tk.RIGHT, padx=10)
        self.progress_bar.start(10)
        
        # Log temizle
        self.log_text.delete(1.0, tk.END)
        
        # Ayrı thread'de eğit
        thread = threading.Thread(target=self.train_model, args=(params,))
        thread.daemon = True
        thread.start()
    
    def train_model(self, params):
        """
        Model eğitimini yap
        """
        try:
            self.log(f"{'='*50}", "info")
            self.log(f"🚀 EĞİTİM BAŞLIYOR", "success")
            self.log(f"{'='*50}", "info")
            self.log(f"📊 Hisse: {params['ticker']}", "info")
            self.log(f"📅 Periyot: {params['period']}", "info")
            self.log(f"🧠 Model: {params['num_layers']}-katmanlı LSTM (size={params['hidden_size']})", "info")
            self.log(f"🔄 Epoch: {params['epochs']}, Batch: {params['batch_size']}", "info")
            
            # 1. Veri toplama
            self.log("\n📥 Veri indiriliyor...", "info")
            df = download_stock_data(ticker=params['ticker'], period=params['period'])
            prices = get_close_prices(df)
            self.log(f"✅ {len(prices)} veri noktası indirildi", "success")
            
            if not self.is_training:
                return
            
            # 2. Veri ön işleme
            self.log("\n🔄 Veri işleniyor...", "info")
            preprocessor = StockDataPreprocessor(lookback=params['lookback'])
            data_dict = preprocessor.prepare_data(prices)
            self.log("✅ Veri hazırlandı", "success")
            
            if not self.is_training:
                return
            
            # 3. Model oluşturma
            self.log("\n🧠 Model oluşturuluyor...", "info")
            model = LSTMStockPredictor(
                hidden_size=params['hidden_size'],
                num_layers=params['num_layers']
            )
            self.log(f"✅ Model hazır (Parametreler: {sum(p.numel() for p in model.parameters()):,})", "success")
            
            if not self.is_training:
                return
            
            # 4. Eğitim
            self.log(f"\n🎯 Eğitim başlıyor ({params['epochs']} epoch)...", "info")
            trainer = StockModelTrainer(model, learning_rate=params['learning_rate'], 
                                       batch_size=params['batch_size'])
            
            history = trainer.train(
                data_dict['X_train'], data_dict['y_train'],
                data_dict['X_test'], data_dict['y_test'],
                epochs=params['epochs'],
                verbose=False
            )
            
            if not self.is_training:
                return
            
            # 5. Tahmin
            self.log("\n📊 Tahminler yapılıyor...", "info")
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            predictions = make_predictions(model, data_dict['X_test'], device=device)
            
            y_test_actual = data_dict['scaler'].inverse_transform(data_dict['y_test'].numpy())
            predictions_actual = data_dict['scaler'].inverse_transform(predictions)
            
            metrics = calculate_metrics(y_test_actual, predictions_actual)
            
            # 6. Kaydetme
            ticker = params['ticker']
            trainer.save_model(f'{ticker}_model.pth')
            plot_training_history(history['train_losses'], history['val_losses'],
                                 save_path=f'{ticker}_training_history.png')
            plot_predictions(y_test_actual.flatten(), predictions_actual.flatten(),
                           ticker=ticker, save_path=f'{ticker}_predictions.png')
            plot_predictions_zoomed(y_test_actual.flatten(), predictions_actual.flatten(),
                                   ticker=ticker, save_path=f'{ticker}_predictions_zoomed.png')
            
            # Sonuç
            self.log(f"\n{'='*50}", "success")
            self.log("✅ EĞİTİM TAMAMLANDI!", "success")
            self.log(f"{'='*50}", "success")
            self.log(f"📊 RMSE: ${metrics['RMSE']:.2f}", "success")
            self.log(f"📊 MAE: ${metrics['MAE']:.2f}", "success")
            self.log(f"📊 MAPE: {metrics['MAPE']:.2f}%", "success")
            self.log(f"📊 R² Score: {metrics['R2']:.4f}", "success")
            self.log(f"\n💾 Dosyalar kaydedildi:", "info")
            self.log(f"   • {ticker}_model.pth", "info")
            self.log(f"   • {ticker}_predictions.png", "info")
            self.log(f"   • {ticker}_training_history.png", "info")
            
            self.training_complete()
            
        except Exception as e:
            self.log(f"\n❌ HATA: {str(e)}", "error")
            self.training_complete()
    
    def stop_training(self):
        """
        Eğitimi durdur
        """
        self.is_training = False
        self.log("\n⛔ Eğitim durduruldu", "warning")
        self.training_complete()
    
    def training_complete(self):
        """
        Eğitim tamamlandı
        """
        self.is_training = False
        self.train_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.update_status("✅ Hazır", self.success_color)
    
    def open_results(self):
        """
        Sonuç dosyalarını aç
        """
        ticker = self.ticker_entry.get().upper().strip()
        files = [
            f'{ticker}_predictions.png',
            f'{ticker}_training_history.png',
            f'{ticker}_predictions_zoomed.png'
        ]
        
        found = False
        for file in files:
            if os.path.exists(file):
                os.startfile(file)  # Windows için
                found = True
        
        if not found:
            messagebox.showinfo("Bilgi", "Henüz sonuç dosyası yok. Önce eğitim yapın.")


def main():
    """
    Uygulamayı başlat
    """
    root = tk.Tk()
    app = StockPredictionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
