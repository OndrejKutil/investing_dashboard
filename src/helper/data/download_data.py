import pandas as pd
import yfinance as yf

def fetch_price_data(ticker: str, period: str = '5y', interval: str = '1d') -> pd.DataFrame:
    """
    Fetch historical price data for a given stock ticker using yfinance.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period to download. 
            Possible values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
            Defaults to '5y'.
        interval (str, optional): Data interval. 
            Possible values: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'.
            Defaults to '1d'.

    Raises:
        ValueError: If no price column is found in the downloaded data.

    Returns:
        pd.DataFrame: DataFrame with date as index and adjusted close prices for the ticker.
    """
    
    data: pd.DataFrame = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    
    # Flatten MultiIndex columns if they exist (yfinance creates MultiIndex when downloading)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in data.columns]

    if f'Close_{ticker}' in data.columns:
        price: pd.DataFrame = data[[f'Close_{ticker}']].rename(columns={f'Close_{ticker}': ticker})
    else:
        raise ValueError("No price column found in downloaded data.")
    
    price.index.name = 'Date'
    return price


def fetch_comprehensive_data(ticker: str, period: str = '5y', interval: str = '1d') -> pd.DataFrame:
    """
    Fetch comprehensive historical data including price, volume, and OHLC data.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        period (str, optional): Data period to download. 
            Possible values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
            Defaults to '5y'.
        interval (str, optional): Data interval. 
            Possible values: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'.
            Defaults to '1d'.

    Returns:
        pd.DataFrame: DataFrame with date as index and OHLCV data for the ticker.
    """
    
    data: pd.DataFrame = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    
    # Flatten MultiIndex columns if they exist (yfinance creates MultiIndex when downloading)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in data.columns]

    # Prepare the columns we want to keep
    result_columns = {}
    
    # Price data (required)
    if f'Close_{ticker}' in data.columns:
        result_columns[ticker] = f'Close_{ticker}'
    elif 'Close' in data.columns:
        result_columns[ticker] = 'Close'
    else:
        raise ValueError("No price column found in downloaded data.")
    
    # Volume data (if available)
    if f'Volume_{ticker}' in data.columns:
        result_columns[f'Volume'] = f'Volume_{ticker}'
    elif 'Volume' in data.columns:
        result_columns[f'Volume'] = 'Volume'
    
    # OHLC data (if available)
    for col_type in ['Open', 'High', 'Low']:
        if f'{col_type}_{ticker}' in data.columns:
            result_columns[f'{col_type}'] = f'{col_type}_{ticker}'
        elif col_type in data.columns:
            result_columns[f'{col_type}'] = col_type
    
    # Create result DataFrame with selected columns
    result = data[[result_columns[key] for key in result_columns]].rename(columns={v: k for k, v in result_columns.items()})
    
    result.index.name = 'Date'
    return result


def fetch_benchmark_data(ticker: str = 'URTH', period: str = '5y', interval: str = '1d') -> pd.DataFrame:
    """
    Fetch historical price data for a benchmark ETF/index.

    Args:
        ticker (str, optional): Benchmark ticker symbol. 
            Popular options: 'URTH' (iShares MSCI World), 'SPY' (S&P 500), 'IWM' (Russell 2000),
            'VGK' (Vanguard Europe), 'PX' (Prague Stock Exchange Index).
            Defaults to 'URTH'.
        period (str, optional): Data period to download. 
            Possible values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
            Defaults to '5y'.
        interval (str, optional): Data interval. 
            Possible values: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'.
            Defaults to '1d'.

    Raises:
        ValueError: If no price column is found in the downloaded data.

    Returns:
        pd.DataFrame: DataFrame with date as index and adjusted close prices labeled as 'benchmark'.
    """
    
    data: pd.DataFrame = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    
    # Flatten MultiIndex columns if they exist (yfinance creates MultiIndex when downloading)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in data.columns]

    if f'Close_{ticker}' in data.columns:
        price: pd.DataFrame = data[[f'Close_{ticker}']].rename(columns={f'Close_{ticker}': 'benchmark'})
    elif 'Close' in data.columns:
        price: pd.DataFrame = data[['Close']].rename(columns={'Close': 'benchmark'})
    else:
        raise ValueError("No price column found in downloaded data.")
    
    price.index.name = 'Date'

    price['benchmark_cumulative_return'] = (1 + price['benchmark'].pct_change()).cumprod() - 1

    return price


def fetch_pe_ratio(ticker: str) -> float:
    """
    Fetch forward P/E ratio for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol.
        
    Returns:
        float: Forward P/E ratio, or None if not available.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Try to get forward P/E ratio, fall back to trailing P/E if not available
        forward_pe = info.get('forwardPE')
        if forward_pe is not None:
            return forward_pe
        
        trailing_pe = info.get('trailingPE')
        if trailing_pe is not None:
            return trailing_pe
            
        return None
    except Exception:
        return None


def fetch_trailing_pe_ratio(ticker: str) -> float:
    """
    Fetch trailing P/E ratio for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol.
        
    Returns:
        float: Trailing P/E ratio, or None if not available.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        trailing_pe = info.get('trailingPE')
        return trailing_pe
    except Exception:
        return None


def fetch_forward_pe_ratio(ticker: str) -> float:
    """
    Fetch forward P/E ratio for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol.
        
    Returns:
        float: Forward P/E ratio, or None if not available.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        forward_pe = info.get('forwardPE')
        return forward_pe
    except Exception:
        return None