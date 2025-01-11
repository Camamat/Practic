import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    threshold = float(input("Введите порог колебаний в процентах (например, 10 для 10%): "))
    csv_filename = input("Введите имя файла для экспорта данных в CSV (например, 'data.csv'): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Checking for fluctuations
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Calculate the average value of the 'Close' column
    dd.calculate_and_display_average_price(stock_data)

    # Export data to CSV
    dd.export_data_to_csv(stock_data, csv_filename)

    # Добавление RSI, MACD
    stock_data = dd.calculate_rsi(stock_data)  # Добавляем расчет RSI
    stock_data = dd.calculate_macd(stock_data)  # Добавляем расчет MACD
    print(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)


if __name__ == "__main__":
    main()
