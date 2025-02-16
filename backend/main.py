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
    return weather.get_weather(), current_time.get_time_period()
    #return weather
    #current_time.get_time_period()

@app.post("/video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = add_ads_to_firebase.FirebaseUploader()
    try:
        
        print("in endpoint...")
        add_ads.upload_video(file)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except Exception as e:
        return JSONResponse(content={"message": f"Video upload failed: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)