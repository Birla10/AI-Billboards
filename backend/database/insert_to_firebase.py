import os
from dotenv import load_dotenv
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, storage
from google.cloud.exceptions import GoogleCloudError, NotFound, Forbidden, ServiceUnavailable

from exceptions.firebase_upload_failed_exception import FirebaseUploadFailedException
from exceptions.file_save_error_exception import FileSaveErrorException

class FirebaseUploader:
    
    def __init__(self):
        load_dotenv()
        self.bucket_name = os.getenv('FIREBASE_STORAGE_BUCKET')
        self.bucker_folder = os.getenv('FIREBASE_ADS_FOLDER')
        self.firestore_collection_id = os.getenv('FIRESTORE_COLLECTION_ID')
        
        # Initialize Firebase App only once
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
            firebase_admin.initialize_app(cred, {
                'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET') 
        })
        
        # Get storage bucket reference
        self.firebase_bucket = storage.bucket()

    def upload_ad_to_firebase_storage(self, file_path):
        """
        Upload the ad file to Firebase Storage and store the tags in Firestore.
        :param file_path: The path of the file to upload.
        :param tags: The tags to store in Firestore.
        """        
        try: 
            if not file_path:
                raise Exception("File could not be saved.")
                
            destination_blob_name = self.bucker_folder + Path(file_path).name
        
            blob = self.firebase_bucket.blob(destination_blob_name)
        
            # Upload the file
            blob.upload_from_filename(file_path)
            
            print("inserted to firebase")
        
            # Return the URL of the uploaded file
            return f"gs://{self.bucket_name}/{destination_blob_name}"
        
        except (GoogleCloudError, NotFound, Forbidden, ServiceUnavailable) as e:
            raise FirebaseUploadFailedException("Failed to upload to Firebase", errors=str(e))
        except (FileNotFoundError, OSError, PermissionError) as e:
            raise FileSaveErrorException(f"File save failed: {str(e)}")
        except Exception as e:
            raise FirebaseUploadFailedException(f"Unexpected error: {str(e)}")
