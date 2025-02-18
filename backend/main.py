from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from data_fetching.weather import WeatherService
from data_fetching.currentTime import TimeClassifier
from database import process_new_ads

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get("/endpoint")
async def read_endpoint():
    print("Endpoint called")
    weather = WeatherService()
    current_time = TimeClassifier()
    return weather.get_weather(), current_time.get_time_period()
    #return weather
    #current_time.get_time_period()

@app.post("/video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = process_new_ads.ProcessNewAds()
    try:
        add_ads.process_ad(file)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except Exception as e:
        return JSONResponse(content={"message": f"Video upload failed: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)