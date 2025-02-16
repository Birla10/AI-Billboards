from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from services.weather import WeatherService
from services.currentTime import TimeClassifier

app = FastAPI()

@app.get("/endpoint")
async def read_endpoint():
    print("Endpoint called")
    weather = WeatherService()
    current_time = TimeClassifier()
    print(weather.get_weather())
    return current_time.get_time_period()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)