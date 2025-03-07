import asyncio
import os
from dotenv import load_dotenv
from datetime import timedelta

import firebase_admin
from firebase_admin import credentials, storage

from services import websocket_service

class FirebaseVideoFetcher:
    def __init__(self):
        
        load_dotenv()
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
            firebase_admin.initialize_app(cred, {
                'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET') 
        })
        
        # Get storage bucket reference
        self.bucket = storage.bucket()

    async def fetch_videos(self, ads):
        """
        Fetches all video URLs from Firebase Storage.
        Returns a list of signed URLs valid for 1 hour.
        """
        
        file_name = f"video_ads/{ads[0]}.mp4"
        blob = self.bucket.blob(file_name)
        
        signed_url = blob.generate_signed_url(expiration=timedelta(hours=1), method='GET')

        asyncio.create_task(websocket_service.send_message(signed_url))
        

