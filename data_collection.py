"""
Hisse senedi verilerini yfinance kullanarak çekme modülü
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def download_stock_data(ticker='AAPL', period='5y', interval='1d'):
    """
    Belirtilen hisse senedi için geçmiş fiyat verilerini indir
    
    Args:
        ticker (str): Hisse senedi sembolü (örn: 'AAPL', 'TSLA')
        period (str): Veri çekme periyodu (örn: '1y', '5y', '10y')
        interval (str): Veri aralığı (örn: '1d', '1h', '1wk')
    
    Returns:
        pd.DataFrame: Hisse senedi fiyat verileri
    """
    print(f"📊 {ticker} için veri indiriliyor...")
    print(f"   Periyot: {period}, Aralık: {interval}")
    
    try:
        # Hisse senedi verisini indir
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            raise ValueError(f"{ticker} için veri bulunamadı!")
        
        print(f"✅ {len(df)} adet veri noktası indirildi")
        print(f"   Tarih Aralığı: {df.index[0].date()} - {df.index[-1].date()}")
        print(f"   Kolonlar: {', '.join(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Hata: {e}")
        raise


def get_close_prices(df):
    """
    DataFrame'den sadece kapanış fiyatlarını al
    
    Args:
        df (pd.DataFrame): Hisse senedi verileri
    
    Returns:
        pd.Series: Kapanış fiyatları
    """
    if 'Close' not in df.columns:
        raise ValueError("Veri setinde 'Close' kolonu bulunamadı!")
    
    close_prices = df['Close'].values
    print(f"📈 Kapanış fiyatları alındı: {len(close_prices)} veri noktası")
    print(f"   Min: ${close_prices.min():.2f}, Max: ${close_prices.max():.2f}")
    print(f"   Ortalama: ${close_prices.mean():.2f}")
    
    return close_prices


if __name__ == "__main__":
    # Test
    df = download_stock_data('AAPL', period='5y')
    prices = get_close_prices(df)
    print(f"\nİlk 5 fiyat: {prices[:5]}")
    print(f"Son 5 fiyat: {prices[-5:]}")
