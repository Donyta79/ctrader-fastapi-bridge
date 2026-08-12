import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="cTrader Bridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEV_MOCK_MODE = True

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "mode": "Mock Mode (Waiting for cTrader Activation)" if DEV_MOCK_MODE else "Live cTrader Mode"
    }

# Endpoint requested by Hercules for OHLCV bars
@app.get("/api/v1/ohlcv/{symbol}")
async def get_ohlcv(symbol: str, timeframe: str = "D1", bars: int = 1260):
    now = int(time.time())
    one_day = 86400
    bars_list = []
    
    # Base price setup based on symbol
    base_price = 1.0850 if "EUR" in symbol.upper() or "USD" in symbol.upper() else 180.0
    current_price = base_price
    
    # Generate requested historical bars
    start_time = now - (bars * one_day)
    for i in range(bars):
        bar_time = start_time + (i * one_day)
        
        # Simulate slight daily price movements
        change_pct = random.uniform(-0.015, 0.015)
        open_price = current_price
        close_price = round(open_price * (1 + change_pct), 4)
        high_price = round(max(open_price, close_price) * (1 + random.uniform(0.001, 0.005)), 4)
        low_price = round(min(open_price, close_price) * (1 - random.uniform(0.001, 0.005)), 4)
        volume = random.randint(1000, 50000)
        
        bars_list.append({
            "time": bar_time,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        })
        current_price = close_price

    return {
        "status": "ok",
        "symbol": symbol.upper(),
        "bars": bars_list
    }

# Keep original summary endpoint as fallback
@app.get("/api/v1/market-data/{symbol}")
async def get_symbol_data(symbol: str):
    base_price = 1.0850 if "EUR" in symbol.upper() or "USD" in symbol.upper() else 180.0
    return {
        "symbol": symbol.upper(),
        "current_price": base_price,
        "ma21": round(base_price * 0.998, 4),
        "ma55": round(base_price * 0.995, 4),
        "ma233": round(base_price * 0.990, 4),
        "cv_percentage": round(random.uniform(0.8, 1.5), 2),
    }
