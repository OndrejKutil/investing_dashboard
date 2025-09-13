from enum import Enum

class Metrics(str, Enum):
    PRICE = "Price"
    MA_20 = "MA_20"
    MA_50 = "MA_50"
    MA_100 = "MA_100"
    MA_200 = "MA_200"
    DAILY_RETURN = "Daily_Return"
    CUMULATIVE_RETURN = "Cumulative_Return"
    CUMULATIVE_ALL_TIME_HIGH = "Cumulative_All_Time_High"
    DRAWDOWN_FROM_HIGH = "Drawdown_From_High"