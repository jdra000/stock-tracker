from dotenv import load_dotenv
import os

import requests
import asyncio
import aiohttp

load_dotenv()
api_key = os.getenv('API_STOCK_KEY')

class API:
    def __init__(self, api_key):
        self.stocks = ['IBM', 'NVDA', 'SMCI', 'TSLA', 'PARA', 'F']

    async def main(self):
        try: 
            async with aiohttp.ClientSession() as session:
                # Task: fetch multiple data
                async with asyncio.TaskGroup() as tg:
                    tasks = {stock: tg.create_task(self.fetch(session, stock)) for stock in self.stocks}
                results = {stock: task.result() for stock, task in tasks.items()}
                print(results)

                # Task: filter and promediate data
                async with asyncio.TaskGroup() as tg:
                    tasks = [tg.create_task(self.calculate_metrics(session, report)) for report in results.values()]
                metrics = {stock: task.result() for stock, task in zip(self.stocks, tasks)}
                print(metrics)
        except Exception as e:
            print(e)
    
    async def fetch(self, session, stock):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&outputsize=full&apikey={self.api_key}'
        try: 
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f'Error fetching{stock}.')
                    return None
        except Exception as e:
            print(e)

    async def calculate_metrics(self, session, report):
        open_acumulate = 0
        close_acumulate = 0
        print(report)
        try:
            for metric in report:
                open_acumulate += metric['1. open']
                close_acumulate += metric['4. close']
            return open_acumulate/30, close_acumulate/30
        except Exception as e:
            print(e)
        
api = API(api_key)
asyncio.run(api.main())



