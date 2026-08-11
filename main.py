import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ctrader_open_api import Client, EndPoints, TcpProtocol
from ctrader_open_api.messages.OpenApiMessages_pb2 import (
    ProtoOAApplicationAuthReq,
    ProtoOAAccountAuthReq,
    ProtoOAGetTrendbarsReq
)

app = FastAPI(title="cTrader Bridge API")

# Enable CORS so your Hercules Frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Hercules app domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cTrader Credentials from Environment Variables
CLIENT_ID = os.getenv("CTRADER_CLIENT_ID")
CLIENT_SECRET = os.getenv("CTRADER_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN")
ACCOUNT_ID = int(os.getenv("CTRADER_ACCOUNT_ID", "0"))

# Persistent cTrader Client Connection
ctrader_client = Client(EndPoints.PROTOBUF_DEMO_HOST, EndPoints.PROTOBUF_PORT, TcpProtocol)

@app.on_event("startup")
async def startup_event():
    # Start persistent connection to cTrader TCP server
    ctrader_client.startService()
    print("cTrader TCP client service started.")

@app.get("/health")
def health_check():
    return {"status": "online", "ctrader_connected": ctrader_client.isConnected()}

# REST Endpoint that your Hercules (Convex) App will call
@app.get("/api/v1/market-data/{symbol}")
async def get_symbol_data(symbol: str):
    if not ctrader_client.isConnected():
        raise HTTPException(status_code=503, detail="cTrader client disconnected")
    
    # Example response structure for your Watchlist & Seasonality Engine
    return {
        "symbol": symbol,
        "ma21": 1.0850,
        "ma55": 1.0820,
        "ma233": 1.0780,
        "cv_percentage": 1.25,
        "sr_levels": {
            "strong_support": 1.0750,
            "strong_resistance": 1.0920
        }
    }
