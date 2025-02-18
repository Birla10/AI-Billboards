import firebase_admin
from firebase_admin import credentials, storage
from config import firebase_bucket, ai_billboards_db
import os
from dotenv import load_dotenv
from pathlib import Path
from video_processing.videos_to_frames import extract_frames
from ai_analysis.frames_processing import FrameAnalyzer
import shutil

class ProcessNewAds:
    def __init__(self):
        
        load_dotenv()
        self.bucket = firebase_bucket
        self.bucket_name = os.getenv('FIREBASE_STORAGE_BUCKET')
        self.bucker_folder = os.getenv('FIREBASE_ADS_FOLDER')
        self.firestore_collection_id = os.getenv('FIRESTORE_COLLECTION_ID')

    def process_ad(self, file):
        """ 
        Process the uploaded ad file.
        :param file: The uploaded ad file.
        """
                    
        # #Save the ad file locally
        # file_path = self.__save_file(file)
        
        # #Extract frames from the video
        # extract_frames(file_path)
        
        # Analyze the frames to extract tags
        frame_analyzer = FrameAnalyzer()
        tags = frame_analyzer.analyze_all_frames(f"resources/frames/Skin care/")   
        
        # # Upload the video to Firebase
        # self.__upload_ad_to_firebase_storage(file_path, tags)
        
        # #Remove the file after processing
        # os.remove(file_path)
        # shutil.rmtree(f"resources/frames/{Path(file_path).stem}/")  
    
    def __save_file(self, file):
        """
        Save the file to a temporary location.
        :param file: The file to save.
        """        
        
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

            return file_path  # Return the saved file path

        except Exception as e:
            print(f"Error saving file: {e}")
            return None
        
    def __upload_ad_to_firebase_storage(self, file_path, tags):
        """
        Upload the ad file to Firebase Storage and store the tags in Firestore.
        :param file_path: The path of the file to upload.
        :param tags: The tags to store in Firestore.
        """        
        
        if not file_path:
            raise Exception("File could not be saved.")
                
        destination_blob_name = self.bucker_folder + Path(file_path).name
        
        blob = self.bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(file_path)
            
        # Store the tags and image url in Firestore
        doc_ref = ai_billboards_db.collection(self.firestore_collection_id).document(Path(file_path).name)
        doc_ref.set({"tags": tags, "image_url": f"gs://{self.bucket_name}/{destination_blob_name}"})
        
        print("Tags and image URL stored in Firestore.")