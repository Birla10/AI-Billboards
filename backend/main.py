from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from services.perform_ad_search import AdSearch
from services.process_new_ads import ProcessNewAds
from exceptions.video_processing_failed_exception import VideoProcessingFailedException

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get("/endpoint")
async def read_endpoint():
    adSearch = AdSearch()
    try:
        embeds = adSearch.getAccurateAd()
        return JSONResponse(embeds, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ad fetching failed: {str(e)}")

@app.post("/video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = ProcessNewAds()
    try:
        add_ads.process_ad(file)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except VideoProcessingFailedException as e:
        raise HTTPException(status_code=500, detail=f"Video upload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)