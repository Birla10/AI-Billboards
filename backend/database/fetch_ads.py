from config import firebase_bucket
import os
from dotenv import load_dotenv
from datetime import timedelta

class FirebaseVideoFetcher:
    def __init__(self):
        self.bucket = firebase_bucket

    def fetch_videos(self):
        """
        Fetches all video URLs from Firebase Storage.
        Returns a list of signed URLs valid for 1 hour.
        """
        blobs = self.bucket.list_blobs(prefix='videos/')  
        
        video_urls = []
        for blob in blobs:
            # Generate signed URL valid for 1 hour
            signed_url = blob.generate_signed_url(
                expiration=timedelta(hours=1), 
                method="GET"
            )
            video_urls.append(signed_url)

        return video_urls

