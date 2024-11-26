from api import api_functionality
import asyncio

class StockTracker:
    def __init__(self, api):
        self.api = api
        print("""
                ╔══════════════════════════════════════╗
                ║                                      ║
                ║      ████████╗████████╗ ██████╗      ║
                ║      ╚══██╔══╝╚══██╔══╝██╔═══██╗     ║
                ║         ██║      ██║   ██║   ██║     ║
                ║         ██║      ██║   ██║   ██║     ║
                ║         ██║      ██║   ╚██████╔╝     ║
                ║         ╚═╝      ╚═╝    ╚═════╝      ║
                ║                                      ║
                ║          STOCK  TRACKER APP          ║
                ║                                      ║
                ╚══════════════════════════════════════╝
                """)
    
    def initiate(self):
        asyncio.run(self.api.main())

stock_tracker = StockTracker(api_functionality)
stock_tracker.initiate()
