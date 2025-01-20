import yfinance as yf
import plotly.graph_objs as go

def fetch_stock_data(ticker, period, start, end):
    """
    Получает данные об акциях для указанного периода.
    
    ticker: Символ акции, для которой нужно получить данные.
    period: Период данных.
    start: Начальная дата периода данных.
    end: Конечная дата периода данных.

    """
    
    stock = yf.Ticker(ticker)
    if start is not None:
        data = stock.history(start=start, end=end)
    else:
        data = stock.history(period=period)
    print(data)
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

def  export_data_to_csv(data, filename):
    """
    Экспортирует данные в CSV файл.

    data: База данных которую экспортируем.
    filename: Имя файла для сохранения.
    """

    data.to_csv(filename)
    print(f"CSV file created {filename}")

def calculate_rsi(data, window=14):
    """
    Рассчитывает индекс относительной силы (RSI) для данных о ценах акций.

    data: DataFrame с историческими данными о ценах акций
    window: Период расчета RSI
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rsi = gain / loss
    data['RSI'] = 100 - (100 / (1 + rsi))
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает Moving Average Convergence Divergence (MACD) для данных о ценах акций.

    data: DataFrame с историческими данными о ценах акций
    short_window: Период для короткой экспоненциальной скользящей средней (EMA)
    long_window: Период для длинной экспоненциальной скользящей средней (EMA)
    signal_window: Период для сигнальной линии MACD
    """
    data['EMA_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def calculate_standard_deviation(data):
    """
    Принимает DataFrame с данными о цене закрытия акций и вычисляет стандартное отклонение.
    data: Данные о цене закрытия акций.
    """
    
    std_deviation = data['Close'].std(ddof=1)
    print(f'Стандартное отклонение цены закрытия: {std_deviation}')
    return std_deviation

def interactive_chart(stock_data, ticker):
    """Принимает DataFrame и вычисляет среднее значение колонки 'Close'. Результат  выводится в консоль."""
    # Создание графика с использованием Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Цена закрытия'))

    fig.update_layout(title=f'Исторические цены акции {ticker}',
                      xaxis_title='Дата',
                      yaxis_title='Цена закрытия ($)')

    fig.show()
    average_close = stock_data['Close'].mean()
    print(f'Среднее значение колонки "Close": {average_close}')