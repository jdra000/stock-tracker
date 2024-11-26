from dotenv import load_dotenv
import os

import requests
import asyncio
import aiohttp

load_dotenv()
api_key = os.getenv('API_STOCK_KEY')

class API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks = [
            "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "META", "BRK.B", "UNH", "JNJ",
            "XOM", "JPM", "V", "PG", "MA", "HD", "LLY", "ABBV", "CVX", "PEP",
            "KO", "PFE", "MRK", "BAC", "COST", "TMO", "DIS", "AVGO", "ADBE", "CSCO",
            "ABT", "NFLX", "CRM", "ACN", "DHR", "TXN", "LIN", "WMT", "NKE", "VZ",
            "INTC", "NEE", "MS", "MCD", "AMD", "CMCSA", "HON", "UNP", "PM", "BMY",
            "UPS", "RTX", "AMGN", "ORCL", "SCHW", "CVS", "IBM", "LOW", "SPGI", "COP",
            "QCOM", "GS", "PLD", "AXP", "T", "BLK", "CAT", "ELV", "DE", "EL",
            "MMC", "MDLZ", "NOW", "C", "AMT", "ADP", "PYPL", "BKNG", "LMT", "MDT",
            "ISRG", "INTU", "MO", "GILD", "GE", "WM", "SO", "CB", "REGN", "SYK",
            "APD", "ZTS", "EQIX", "CI", "HCA", "KLAC", "VRTX", "ETN", "CSX", "NSC",
            "PGR", "TGT", "DUK", "EW", "BDX", "USB", "SHW", "TJX", "ECL", "ITW",
            "MCO", "BSX", "AON", "AEP", "FISV", "FDX", "ADSK", "PSA", "TFC", "KHC",
            "CARR", "TRV", "PANW", "CTAS", "HUM", "CHTR", "DG", "ROP", "PRU", "WMB",
            "BK", "F", "WFC", "EPAM", "OTIS", "EXC", "CMI", "FMC", "HAL", "LEN",
            "MRNA", "MTB", "NOC", "PH", "PNC", "ROK", "STZ", "TSN", "YUM", "AIG",
            "ALL", "AME", "ATO", "AWK", "BBY", "BLL", "BKR", "CBOE", "CDNS", "CF",
            "CHD", "CHRW", "CL", "CLX", "CMS", "COF", "CPB", "CTSH", "D", "DGX",
            "DLTR", "DOV", "DRE", "EIX", "EMR", "EQR", "ESS", "FDS", "FE", "FFIV",
            "FIS", "FLT", "GL", "GLW", "HES", "HSY", "IFF", "IR", "JKHY", "K",
            "KEY", "KIM", "KMB", "L", "LHX", "LKQ", "LNC", "LYB", "MAS", "MKC",
            "MKTX", "MPWR", "MSI", "NDAQ", "NEM", "NUE", "OKE", "ORLY", "OTTR", "PAYX",
            "PCAR", "PEG", "PEP", "PFG", "PKI", "PNW", "PPG", "PPL", "PXD", "RCL",
            "RF", "RJF", "RMD", "RSG", "SBUX", "SNA", "SNPS", "STT", "STX", "SYY",
            "TDG", "TER", "TFX", "TTWO", "UHS", "UNH", "URI", "VLO", "VMC", "VRSN",
            "VRTX", "VTRS", "WAB", "WAT", "WBA", "WEC", "WRB", "WST", "WY", "XRAY",
            "XYL", "ZBH", "ZION", "ZTS", "ADM", "AFL", "AIZ", "APTV", "BBWI", "BXP",
            "CME", "CMS", "DHI", "DISCK", "DRI", "DXC", "ED", "EFX", "ESS", "FITB",
            "FRC", "HBAN", "HRL", "HST", "ICE", "IPG", "IRM", "JNPR", "KEYS", "LEG",
            "LUMN", "MKC", "NRG", "NVR", "OKE", "PAYC", "QRVO", "RE", "ROL", "SBAC",
            "SIVB", "SPG", "STLD", "SWKS", "TDY", "TPR", "TT", "VFC", "WHR", "XYL"
        ]



    async def main(self):
        try: 
            async with aiohttp.ClientSession() as session:
                # Task: fetch daily data
                async with asyncio.TaskGroup() as tg:
                    tasks = {stock: tg.create_task(self.fetch_daily(session, stock)) for stock in self.stocks}
                results = {stock: {'open_values':task.result()[0], 'closed_values':task.result()[1]} for stock, task in tasks.items()}
                if results:
                    print('--------------------------- DAILY DATA LOADED ---------------------------')

                # Task: fetch weekly data
                async with asyncio.TaskGroup() as tg:
                    tasks = {stock: tg.create_task(self.fetch_weekly(session, stock)) for stock in self.stocks}
                results = {stock: {'open_values': task.result()[0], 'closed_values':task.result()[1]} for stock, task in tasks.items()}
                if results:
                    print('--------------------------- WEEKLY DATA LOADED ---------------------------')
        except Exception as e:
            print(e)
    
    async def fetch_daily(self, session, stock):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={self.api_key}'
        try: 
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
    
                    all_days = data. get('Time Series (Daily)', {})
                    open_values = [value['1. open'] for value in all_days.values()]
                    closed_values = [value['4. close'] for value in all_days.values()]

                    return open_values, closed_values
                else:
                    print(f'Error fetching{stock}.')
                    return None
        except Exception as e:
            print(e)

    async def fetch_weekly(self, session, stock):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock}&apikey={self.api_key}'
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    all_weeks = data.get('Weekly Time Series', {})
                    open_values = [value['1. open'] for value in all_weeks.values()]
                    closed_values = [value['4. close'] for value in all_weeks.values()]

                    return open_values, closed_values
                else:
                    print(f'error fetching stock {stock}.')
                    return None
        except Exception as e:
            print(e)

api_functionality = API(api_key)



