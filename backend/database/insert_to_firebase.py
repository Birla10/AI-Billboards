from pathlib import Path
from config import firebase_bucket, ai_billboards_db
import os
from dotenv import load_dotenv

load_dotenv()
bucket_name = os.getenv('FIREBASE_STORAGE_BUCKET')
bucker_folder = os.getenv('FIREBASE_ADS_FOLDER')
firestore_collection_id = os.getenv('FIRESTORE_COLLECTION_ID')

def upload_ad_to_firebase_storage(self, file_path):
        """
        Upload the ad file to Firebase Storage and store the tags in Firestore.
        :param file_path: The path of the file to upload.
        :param tags: The tags to store in Firestore.
        """        
        
        if not file_path:
            raise Exception("File could not be saved.")
                
        destination_blob_name = bucker_folder + Path(file_path).name
        
        blob = firebase_bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(file_path)
            
        # # Store the tags and image url in Firestore
        # doc_ref = ai_billboards_db.collection(firestore_collection_id).document(Path(file_path).name)
        # doc_ref.set({"tags": tags, "image_url": f"gs://{bucket_name}/{destination_blob_name}"})
        
        print("inserted to firebase")
        
        # Return the URL of the uploaded file
        return f"gs://{bucket_name}/{destination_blob_name}"