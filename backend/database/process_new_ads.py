import firebase_admin
from firebase_admin import credentials, storage
from config import firebase_bucket, ai_billboards_db
import os
from pathlib import Path
from video_processing.videos_to_frames import extract_frames
from ai_analysis.frames_processing import FrameAnalyzer
import shutil

class ProcessNewAds:
    def __init__(self):
        self.bucket = firebase_bucket
        self.bucket_name = os.getenv('FIREBASE_STORAGE_BUCKET')

    def process_ad(self, file, make_public=False):
        """
        Uploads a video to Firebase Storage.

        :param file: The video file to upload.
        :param make_public: If True, makes the file publicly accessible.
        :return: The public URL of the uploaded file (if public), otherwise signed URL.
        """
        
        #Save the ad file locally
        file_path = self.__save_file(file)
        print(f"File path: {file_path}")
        
        #Extract frames from the video
        extract_frames(file_path)
        
        # Analyze the frames to extract tags
        frame_analyzer = FrameAnalyzer()
        tags = frame_analyzer.analyze_all_frames(f"resources/frames/{Path(file_path).stem}/")
        print(f"Extracted tags: {tags}")        
        
        # Upload the video to Firebase Storage
        storage_url = self.__upload_ad_to_firebase_storage(file_path)
        
        # Store the tags and image url in Firestore
        doc_ref = ai_billboards_db.collection(os.getenv('FIRESTORE_COLLECTION_ID')).document(file.filename)
        doc_ref.set({"tags": tags, "image_url": storage_url})
        
        print("Tags and image URL stored in Firestore.")
        
        #Remove the file after processing
        os.remove(file_path)
        shutil.rmtree(f"resources/frames/{Path(file_path).stem}/")  
    
    def __save_file(self, file):
        """
        Save the file to a temporary location.
        :param file: The file to save.
        """        
        print("in save file...")
        
        # Define the target directory
        self.upload_folder = "resources/new_ads/"
        
        # Ensure the directory exists
        os.makedirs(self.upload_folder, exist_ok=True)
        
        try:
            # Define the full path where the file will be saved
            file_path = os.path.join(self.upload_folder, file.filename)

            # Save the uploaded file
            with open(file_path, "wb") as f:
                f.write(file.file.read())

            print(f"File '{file.filename}' saved at '{file_path}'.")
            return file_path  # Return the saved file path

        except Exception as e:
            print(f"Error saving file: {e}")
            return None
        
    def __upload_ad_to_firebase_storage(self, file_path):
        print("Uploading video to Firebase Storage...")
        if not file_path:
            raise Exception("File could not be saved.")
                
        destination_blob_name = os.getenv('FIREBASE_ADS_FOLDER') + Path(file_path).name
        
        print(f"Destination Blob Name: {destination_blob_name}")
        blob = self.bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(file_path)
        return f"gs://{self.bucket_name}/{destination_blob_name}"