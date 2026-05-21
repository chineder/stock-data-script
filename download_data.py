# This script downloads stock price data from Yahoo Finance.
# Run the script to reproduce the dataset used in the paper.
# Dependencies: yfinance, pandas
import yfinance as yf
import pandas as pd
import os
import time

def download_stock_data(stocks, output_dir, start_date, end_date, interval='1d'):
    """
    Download daily stock price data from Yahoo Finance and save as CSV files.

    Parameters
    ----------
    stocks : list of str
        List of stock tickers (e.g., ['AAPL', 'TSLA']).
    output_dir : str
        Directory to save the output CSV files.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    interval : str, optional
        Data interval (default is '1d').

    Returns
    -------
    dict
        A dictionary mapping each stock ticker to its corresponding DataFrame.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_stock_dfs = {}

    for stock in stocks:
        print(f"[INFO] Downloading {stock}...")
        time.sleep(1)

        df = yf.download(stock, start=start_date, end=end_date, interval=interval)

        if df is None or df.empty:
            print(f"[ERROR] No data downloaded for {stock}")
            continue

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[['Close']].reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        csv_path = os.path.join(output_dir, f"{stock}.csv")
        df.to_csv(csv_path, index=False)

        all_stock_dfs[stock] = df

    return all_stock_dfs


if __name__ == "__main__":

    # Example usage
    output_dir = "./close_price"
    stocks = ['AMZN', 'BRK-A', 'INTC', 'KO', 'SBUX', 'TSLA']
    start_date = '2022-01-01'
    end_date = '2024-01-01' # exclusive; data up to last trading day before this date
    interval = '1d'

    download_stock_data(stocks, output_dir, start_date, end_date, interval)
    print(f"[DONE] output_dir: {output_dir}")
