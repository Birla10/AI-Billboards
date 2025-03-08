import uvicorn
import asyncio
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, WebSocket, WebSocketDisconnect

from services.perform_ad_search import AdSearch
from services.process_new_ads import ProcessNewAds
from services.websocket_service import websocket_manager
from exceptions.video_processing_failed_exception import VideoProcessingFailedException

# Create FastAPI app
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/endpoint")
async def read_endpoint():
    adSearch = AdSearch()
    try:
        await adSearch.getAccurateAd()
        return JSONResponse("success", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ad fetching failed: {str(e)}")

@app.post("/video/")
async def upload_video(file: UploadFile = File(...), keywords: list[str] = Form(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = ProcessNewAds()
    try:
        add_ads.process_ad(file, keywords)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except VideoProcessingFailedException as e:
        raise HTTPException(status_code=500, detail=f"Video upload failed: {str(e)}")
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    print("Client connected")

    try:
        while True:
            await asyncio.sleep(1)  # Keep connection open (do nothing)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app)

    
