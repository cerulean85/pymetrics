from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from metrics.yfinance import *
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(root_path="/dev/")

# CORS 설정 (브라우저에서 호출 가능하게)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # 특정 도메인만 허용하려면 리스트로 설정
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/check")
def read_root():
    return {"test":"FastAPI start: Updated By 250517"}

class TickersRequest(BaseModel):
    tickers_periods: Dict[str, str]

class TickerRequest(BaseModel):
    tickers: List[str]

@app.post("/metrics")
def get_metrics(request: TickersRequest):
    data = get_close_data(request.tickers_periods)
    result = {
        'isSuccess': True,
        'message': "Data fetch successful",
        'data': data
    }
    return JSONResponse(content=result)

@app.post("/latest-prices")
def fetch_latest_prices(request: TickerRequest):
    prices = get_latest_prices(request.tickers)
    return {
        "isSuccess": True,
        "message": "Latest price fetch successful",
        "data": prices
    }

handler = Mangum(app)
# if __name__ == "__main__":  
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8005)
    # prices = get_latest_prices([
    #     "PG", "VOOV", "TSM", "NEE", "IWR", "VNQ", "VB", "BRK-B", "BURL", "BLK",
    #     "VWO", "ANET", "AMZN", "AXP", "GOOG", "AAPL", "WMT", "KO", "CL", "KHC", "TSLA", "PM", "HSY"
    # ])