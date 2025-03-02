import os
import shutil
from pathlib import Path

import numpy as np

from video_processing.videos_to_frames import extract_frames
from ai_analysis.cloud_vision_frame_processing import FrameAnalyzer
from ai_analysis.create_embeddings import CreateEmbeddings
from ai_analysis.generate_context_tags import generate_tags
from database.insert_to_firebase import upload_ad_to_firebase_storage
from database.insert_embeddings import InsertEmbeddings 

from exceptions.file_save_error_exception import FileSaveErrorException
from exceptions.video_processing_failed_exception import VideoProcessingFailedException
from exceptions.firebase_upload_failed_exception import FirebaseUploadFailedException
from exceptions.frames_processing_failed_exception import FramesProcessingFailedException
from exceptions.frames_extraction_failed_exception import FramesExtractionFailedException
from exceptions.tags_generation_failed_exception import TagsGenerationFailedException
from exceptions.pinecone_insertion_failure_exception import PineconeInsertionFailureException

class ProcessNewAds:
    """
    Class to process new ads.
    """
    
    def process_ad(self, file):
        """ 
        Processes the uploaded ad file.
    
        Steps:
        1. Saves the file locally.
        2. Uploads it to Firebase.
        3. Extracts frames.
        4. Analyzes frames using AI.
        5. Generates and stores embeddings.

        :param file: Uploaded video file.
        :raises VideoProcessingFailedException: If any step in the process fails.
        """
        try:            
            #Save the ad file locally
            file_path = self.__save_file(file)
            
            print(Path(file_path).name.endswith(('.mp4', '.mov', '.avi')))
            
            if not Path(file_path).name.endswith(('.mp4', '.mov', '.avi')):
                raise VideoProcessingFailedException("Unsupported file format. Please upload a video file.") from None
        
            # Upload the video to Firebase
            storage_url = upload_ad_to_firebase_storage(self, file_path)
            #"gs://ai-billboards-63f04.firebasestorage.app/video_ads/Fashion.mp4"
        
            #Extract frames from the video
            extract_frames(file_path)
        
            # Analyze the frames to extract tags
            frame_analyzer = FrameAnalyzer()
            obj_tags = frame_analyzer.analyze_all_frames(f"resources/frames/{Path(file_path).stem}/")   
        
            #Generate context tags based on obj_tags
            context_tags = generate_tags(obj_tags)
        
            create_embeddings = CreateEmbeddings()
            insert_embeddings = InsertEmbeddings()
        
            #Create and insert object context embeddings
            obj_embeddings = create_embeddings.create_obj_embeddings(list(obj_tags))
            insert_embeddings.insert_to_pinecone(obj_embeddings, list(obj_tags), storage_url, "obj")
        
            #Create and insert context embeddings
            context_embeddings = create_embeddings.create_context_embeddings(file_path)
            insert_embeddings.insert_to_pinecone(context_embeddings, context_tags, storage_url, "context")       
                   
        except (FileSaveErrorException, FirebaseUploadFailedException, FramesExtractionFailedException, FramesProcessingFailedException, TagsGenerationFailedException,PineconeInsertionFailureException) as e:
            raise VideoProcessingFailedException("Video processing failed") from e      
        finally:
            #Remove the file after processing
            os.remove(file_path)
            shutil.rmtree(f"resources/frames/{Path(file_path).stem}/")     
    
    def __save_file(self, file):
        """
        Save the file to a temporary location.
        :param file: The file to save.
        """        
        
        # Define the target directory
        self.upload_folder = "resources/new_ads/"
        
        # Ensure the directory exists
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder, exist_ok=True)
        
        try:
            # Define the full path where the file will be saved
            file_path = os.path.join(self.upload_folder, file.filename)

            # Save the uploaded file
            with open(file_path, "wb") as f:
                f.write(file.file.read())

            return file_path  # Return the saved file path

        except (PermissionError, FileNotFoundError, IsADirectoryError, TypeError, OSError) as e:
            raise FileSaveErrorException(f"File save failed: {str(e)}") from e

        except Exception as e:
            raise FileSaveErrorException(f"Unexpected error: {str(e)}")
        
    