import os
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

# Set to True while waiting for Spotware activation, set to False once Active
DEV_MOCK_MODE = True

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "mode": "Mock Mode (Waiting for cTrader Activation)" if DEV_MOCK_MODE else "Live cTrader Mode"
    }

@app.get("/api/v1/market-data/{symbol}")
async def get_symbol_data(symbol: str):
    # Simulated data so Hercules AI Coder can build the whole UI today
    base_price = 1.0850 if "EUR" in symbol.upper() or "USD" in symbol.upper() else 180.0
    
    return {
        "symbol": symbol.upper(),
        "current_price": base_price,
        "ma21": round(base_price * 0.998, 4),
        "ma55": round(base_price * 0.995, 4),
        "ma233": round(base_price * 0.990, 4),
        "seasonality": {
            "monthly_avg": [1.2, -0.5, 0.8, 1.5, -1.0, 0.4, 0.9, -0.2, -1.1, 0.6, 1.8, 0.3],
            "weekly_avg": [0.4, 0.2, -0.3, 0.5]
        },
        "cv_percentage": round(random.uniform(0.8, 1.5), 2),
        "projected_range": {
            "low": round(base_price * 0.991, 4),
            "high": round(base_price * 1.009, 4)
        },
        "sr_levels": {
            "h4": {"strong_support": round(base_price * 0.985, 4), "strong_resistance": round(base_price * 1.015, 4)},
            "daily": {"strong_support": round(base_price * 0.975, 4), "strong_resistance": round(base_price * 1.025, 4)}
        }
    }
