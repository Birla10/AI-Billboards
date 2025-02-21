from video_processing.videos_to_frames import extract_frames
from ai_analysis.cloud_vision_frame_processing import FrameAnalyzer
from ai_analysis.create_embeddings import CreateEmbeddings
from database.insert_embeddings import InsertEmbeddings
from database.insert_to_firebase import upload_ad_to_firebase_storage
from ai_analysis.generate_context_tags import generate_tags
from pathlib import Path
import numpy as np
import os
import shutil

class ProcessNewAds:
    """
    Class to process new ads.
    """
    
    def process_ad(self, file):
        """ 
        Process the uploaded ad file.
        :param file: The uploaded ad file.
        """
        
        #Save the ad file locally
        file_path = self.__save_file(file)
        
        # # Upload the video to Firebase
        # storage_url = upload_ad_to_firebase_storage(file_path, obj_tags)
        
        #Extract frames from the video
        extract_frames(file_path)
        
        # Analyze the frames to extract tags
        frame_analyzer = FrameAnalyzer()
        obj_tags = frame_analyzer.analyze_all_frames(f"resources/frames/{Path(file_path).stem}/")   
        # context_tags = generate_tags(obj_tags)
        
        print(obj_tags)
        
        create_embeddings = CreateEmbeddings()
        # obj_embeddings = create_embeddings.create_obj_embeddings(list(obj_tags))
        # context_embeddings = create_embeddings.create_context_embeddings(file_path)
        
        # insert_embeddings = InsertEmbeddings()
        # insert_embeddings.insert_to_pinecone(obj_embeddings, obj_tags, context_embeddings, context_tags, storage_url)
        
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
        
    