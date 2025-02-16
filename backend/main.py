from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from data_fetching.weather import WeatherService
from data_fetching.currentTime import TimeClassifier
from database import add_ads_to_firebase

app = FastAPI()

@app.get("/endpoint")
async def read_endpoint():
    print("Endpoint called")
    weather = WeatherService()
    current_time = TimeClassifier()
    print(weather.get_weather())
    return current_time.get_time_period()

@app.post("/video/")
async def upload_video(file: UploadFile):
    """
    Endpoint to upload a video file.
    """
    add_ads = add_ads_to_firebase.FirebaseUploader()
    try:
        add_ads.upload_video(file.file)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except Exception as e:
        return JSONResponse(content={"message": f"Video upload failed: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)