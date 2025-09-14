import pandas as pd


def add_statistics(data: pd.DataFrame, ticker: str = None) -> pd.DataFrame:
    """
    Add statistical columns to the DataFrame including moving averages,
    daily returns, cumulative returns, cumulative all-time high, and drawdown from high.
    Always calculates all available metrics. Preserves existing benchmark columns.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.
        ticker (str): Stock ticker symbol for fetching P/E ratio (optional).

    Returns:
        pd.DataFrame: DataFrame with additional statistical columns.
    """
    # Store any existing benchmark columns to preserve them
    
    data = add_moving_averages(data, windows=[20, 50, 100, 200])
    data = add_daily_returns(data)
    data = add_cumulative_returns(data)
    data = add_cummulative_all_time_high(data)
    data = add_drawdown_from_high(data)

    
    return data


def add_moving_averages(data: pd.DataFrame, windows: list[int]) -> pd.DataFrame:
    """
    Add moving average columns to the DataFrame for specified window sizes.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.
        windows (list[int]): List of window sizes for moving averages.

    Returns:
        pd.DataFrame: DataFrame with additional moving average columns.
    """
    data = data.copy()  # Create a copy to avoid SettingWithCopyWarning
    for window in windows:
        ma_column = f'MA_{window}'
        data.loc[:, ma_column] = data.iloc[:, 0].rolling(window=window).mean()
    return data

def add_daily_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a daily returns column to the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.

    Returns:
        pd.DataFrame: DataFrame with an additional daily returns column.
    """
    data['Daily_Return'] = data.iloc[:, 0].pct_change()
    return data

def add_cumulative_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a cumulative returns column to the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.

    Returns:
        pd.DataFrame: DataFrame with an additional cumulative returns column.
    """
    data['Cumulative_Return'] = (1 + data.iloc[:, 0].pct_change()).cumprod() - 1
    return data

def add_cummulative_all_time_high(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a cumulative all-time high column to the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.

    Returns:
        pd.DataFrame: DataFrame with an additional cumulative all-time high column.
    """
    data['Cumulative_All_Time_High'] = data.iloc[:, 0].cummax()
    return data

def add_drawdown_from_high(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a drawdown from high column to the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with date as index and price data.

    Returns:
        pd.DataFrame: DataFrame with an additional drawdown from high column.
    """
    data['Drawdown_From_High'] = data.iloc[:, 0] / data.iloc[:, 0].cummax() - 1
    data['Drawdown_Percentile'] = data['Drawdown_From_High'].rank(pct=True)
    return data







