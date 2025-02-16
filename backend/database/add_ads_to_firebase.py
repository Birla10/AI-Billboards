import firebase_admin
from firebase_admin import credentials, storage
from config import firebase_bucket
import os
from pathlib import Path

class FirebaseUploader:
    def __init__(self):
        self.bucket = firebase_bucket

    def upload_video(self, file, make_public=False):
        """
        Uploads a video to Firebase Storage.

        :param file: The video file to upload.
        :param make_public: If True, makes the file publicly accessible.
        :return: The public URL of the uploaded file (if public), otherwise signed URL.
        """
        
        file_path = self.__save_file(file)
        
        print("Uploading video to Firebase Storage...")
        if not file_path:
            raise Exception("File could not be saved.")
                
        destination_blob_name = 'new_ads/' + Path(file_path).name
        
        print(f"Destination Blob Name: {destination_blob_name}")
        blob = self.bucket.blob(destination_blob_name)

        print("Blob created.")
        # Upload the file
        blob.upload_from_filename(file_path)
        print(f'File {Path(file_path).name} uploaded to {destination_blob_name}.')

        os.remove(file_path)  # Remove the file after uploading
        
        # Otherwise, generate a signed URL (valid for 1 hour)
        return blob.generate_signed_url(expiration=3600)

    
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
            print(f"❌ Error saving file: {e}")
            return None