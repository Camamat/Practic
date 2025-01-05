import yfinance as yf


def fetch_stock_data(ticker, period="1mo"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data["Moving_Average"] = data["Close"].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    data: Принимает БД с данными по запрошенной акции
    average: Принимает среднее значение колонки Close
    """
    average = data["Close"].mean()
    return average


def notify_if_strong_fluctuations(data, threshold):
    """

    data: Принимает БД с данными по запрошенной акции
    threshold: Принимает пороговое значение колебаний в процентах от средней цены закрытия за указанный период
    return: Уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период
    """
    min_price = data["Close"].min()
    max_price = data["Close"].max()

    difference = max_price - min_price
    percent = difference / (calculate_and_display_average_price(data) / 100)
    if percent >= threshold:
        print("Цена акций колебалась более чем на заданный процент!")
