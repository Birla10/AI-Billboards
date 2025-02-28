from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from services.perform_ad_search import AdSearch
from services.process_new_ads import ProcessNewAds

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get("/endpoint")
async def read_endpoint():
    adSearch = AdSearch()
    try:
        embeds = adSearch.getAccurateAd()
        return JSONResponse(embeds, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed: {str(e)}"}, status_code=500)

@app.post("/video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = ProcessNewAds()
    try:
        add_ads.process_ad(file)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except Exception as e:
        return JSONResponse(content={"message": f"Video upload failed: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)