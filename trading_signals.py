"""
AL/SAT Sinyalleri - Trading Stratejisi
"""
import numpy as np
import pandas as pd


class TradingSignalGenerator:
    """
    Tahminlere göre AL/SAT sinyalleri üretir
    """
    
    def __init__(self, threshold_percent=2.0):
        """
        Args:
            threshold_percent (float): AL/SAT için minimum yüzde değişim
        """
        self.threshold_percent = threshold_percent
    
    def generate_signals(self, current_prices, predictions):
        """
        AL/SAT sinyalleri üret
        
        Args:
            current_prices (np.array): Bugünün fiyatları
            predictions (np.array): Yarının tahmin edilen fiyatları
        
        Returns:
            list: Her gün için sinyal (BUY, HOLD, SELL)
        """
        signals = []
        percentages = []
        
        for current, predicted in zip(current_prices, predictions):
            # Yüzdesel değişim
            change_percent = ((predicted - current) / current) * 100
            percentages.append(change_percent)
            
            # Sinyal üret
            if change_percent >= self.threshold_percent:
                signal = "🟢 AL (BUY)"
                emoji = "📈"
            elif change_percent <= -self.threshold_percent:
                signal = "🔴 SAT (SELL)"
                emoji = "📉"
            else:
                signal = "⚪ BEKLE (HOLD)"
                emoji = "➡️"
            
            signals.append({
                'signal': signal,
                'emoji': emoji,
                'change_percent': change_percent,
                'current_price': current,
                'predicted_price': predicted,
                'reason': self._get_reason(change_percent)
            })
        
        return signals, percentages
    
    def _get_reason(self, change_percent):
        """Sinyal sebebini açıkla"""
        if change_percent >= 5:
            return "Güçlü yükseliş bekleniyor"
        elif change_percent >= 2:
            return "Hafif yükseliş bekleniyor"
        elif change_percent <= -5:
            return "Güçlü düşüş bekleniyor"
        elif change_percent <= -2:
            return "Hafif düşüş bekleniyor"
        else:
            return "Önemli değişim beklenmiyor"
    
    def get_latest_signal(self, current_price, predicted_price):
        """
        En son (bugünkü) AL/SAT sinyali
        
        Args:
            current_price (float): Bugünün kapanış fiyatı
            predicted_price (float): Yarın için tahmin
        
        Returns:
            dict: Sinyal bilgisi
        """
        change_percent = ((predicted_price - current_price) / current_price) * 100
        
        if change_percent >= self.threshold_percent:
            signal = "🟢 AL (BUY)"
            emoji = "📈"
            action = "AL"
            color = "green"
        elif change_percent <= -self.threshold_percent:
            signal = "🔴 SAT (SELL)"
            emoji = "📉"
            action = "SAT"
            color = "red"
        else:
            signal = "⚪ BEKLE (HOLD)"
            emoji = "➡️"
            action = "BEKLE"
            color = "gray"
        
        return {
            'signal': signal,
            'action': action,
            'emoji': emoji,
            'color': color,
            'change_percent': change_percent,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'reason': self._get_reason(change_percent),
            'confidence': self._calculate_confidence(abs(change_percent))
        }
    
    def _calculate_confidence(self, abs_change):
        """Güven seviyesi hesapla"""
        if abs_change >= 5:
            return "Yüksek"
        elif abs_change >= 3:
            return "Orta"
        elif abs_change >= 1:
            return "Düşük"
        else:
            return "Çok Düşük"
    
    def generate_summary(self, signals):
        """
        Sinyal özeti
        
        Args:
            signals (list): Sinyal listesi
        
        Returns:
            dict: Özet istatistikler
        """
        buy_count = sum(1 for s in signals if "AL" in s['signal'])
        sell_count = sum(1 for s in signals if "SAT" in s['signal'])
        hold_count = sum(1 for s in signals if "BEKLE" in s['signal'])
        
        avg_change = np.mean([s['change_percent'] for s in signals])
        
        return {
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'hold_signals': hold_count,
            'total_signals': len(signals),
            'average_change': avg_change,
            'buy_percentage': (buy_count / len(signals)) * 100,
            'sell_percentage': (sell_count / len(signals)) * 100,
            'hold_percentage': (hold_count / len(signals)) * 100
        }


def print_latest_signal(ticker, current_price, predicted_price, threshold=2.0):
    """
    En son sinyali yazdır
    
    Args:
        ticker (str): Hisse sembolü
        current_price (float): Bugünün fiyatı
        predicted_price (float): Yarının tahmini
        threshold (float): AL/SAT eşiği (%)
    """
    generator = TradingSignalGenerator(threshold_percent=threshold)
    signal = generator.get_latest_signal(current_price, predicted_price)
    
    print(f"\n{'='*60}")
    print(f"📊 {ticker} İÇİN AL/SAT SİNYALİ")
    print(f"{'='*60}")
    print(f"📅 Bugünün Fiyatı:       ${signal['current_price']:.2f}")
    print(f"🔮 Yarın Tahmini:        ${signal['predicted_price']:.2f}")
    print(f"📈 Beklenen Değişim:     {signal['change_percent']:+.2f}%")
    print(f"{'='*60}")
    print(f"{signal['emoji']} SİNYAL: {signal['action']}")
    print(f"💡 Sebep: {signal['reason']}")
    print(f"🎯 Güven: {signal['confidence']}")
    print(f"{'='*60}\n")
    
    return signal


def print_signal_summary(signals, ticker):
    """
    Sinyal özetini yazdır
    
    Args:
        signals (list): Sinyal listesi
        ticker (str): Hisse sembolü
    """
    generator = TradingSignalGenerator()
    summary = generator.generate_summary(signals)
    
    print(f"\n{'='*60}")
    print(f"📊 {ticker} SİNYAL ÖZETİ ({summary['total_signals']} Gün)")
    print(f"{'='*60}")
    print(f"🟢 AL Sinyali:    {summary['buy_signals']:3d} gün ({summary['buy_percentage']:.1f}%)")
    print(f"🔴 SAT Sinyali:   {summary['sell_signals']:3d} gün ({summary['sell_percentage']:.1f}%)")
    print(f"⚪ BEKLE Sinyali: {summary['hold_signals']:3d} gün ({summary['hold_percentage']:.1f}%)")
    print(f"📈 Ort. Değişim:  {summary['average_change']:+.2f}%")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Test
    print("🧪 Trading Signal Generator Testi\n")
    
    # Örnek veri
    current_prices = np.array([150, 152, 151, 155, 154])
    predictions = np.array([153, 150, 152, 160, 152])
    
    generator = TradingSignalGenerator(threshold_percent=2.0)
    signals, percentages = generator.generate_signals(current_prices, predictions)
    
    # Sinyalleri yazdır
    for i, (signal, pct) in enumerate(zip(signals, percentages)):
        print(f"Gün {i+1}: {signal['signal']:20s} | "
              f"${signal['current_price']:.2f} → ${signal['predicted_price']:.2f} "
              f"({pct:+.2f}%)")
    
    # Özet
    print_signal_summary(signals, "TEST")
    
    # En son sinyal
    print_latest_signal("TEST", current_prices[-1], predictions[-1])
    
    print("✅ Test tamamlandı!")
