import yfinance as yf
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_close_data(tickers_periods):
    """
    tickers_periods: dict, key=티커 심볼, value=조회 기간 (예: '3mo', '1mo')
    반환: dict, key=티커, value=종가 리스트 [{"date": "YYYY-MM-DD", "value": float}, ...]
    """
    result = {}
    for ticker_symbol, period in tickers_periods.items():
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period=period)
        close_data = [{"date": str(date.date()), "value": round(close, 2)} for date, close in data['Close'].items()]
        result[ticker_symbol] = close_data
    return result



def fetch_price(ticker: str) -> Optional[float]:
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if 'Close' in data and not data['Close'].dropna().empty:
            return round(data['Close'].dropna().iloc[-1], 2)
    except Exception:
        pass
    return None

import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional

def get_latest_prices(tickers: List[str]) -> Dict[str, Optional[float]]:
    results: Dict[str, Optional[float]] = {}
    usd_ticker = "USDKRW=X"
    all_tickers = list(set(tickers + [usd_ticker]))

    try:
        data = yf.download(all_tickers, period="1d", interval="1m", progress=False)
        # print("Downloaded data:")
        # print(data.head())
    except Exception as e:
        print("Download error:", e)
        return {}

    if data.empty:
        print("No data")
        return results

    for ticker in all_tickers:
        try:
            if ('Close', ticker) in data.columns:
                close_series = data['Close'][ticker].dropna()
                if not close_series.empty:
                    results[ticker] = float(round(close_series.iloc[-1], 2))
            else:
                print(f"{ticker} has no 'Close' data")
        except Exception as e:
            print(f"{ticker} error: {e}")

    return results


if __name__ == "__main__":
    result = get_latest_prices([
        "PG", "VOOV", "TSM", "NEE", "IWR", "VNQ", "VB", "BRK-B", "BURL", "BLK",
        "VWO", "ANET", "AMZN", "AXP", "GOOG", "AAPL", "WMT", "KO", "CL", "KHC", "TSLA", "PM", "HSY"
    ])
    print(result)