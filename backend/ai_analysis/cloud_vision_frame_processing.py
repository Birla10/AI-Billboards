import os

from google.cloud import vision

from exceptions.frames_processing_failed_exception import FramesProcessingFailedException
from exceptions.image_processing_failed_exception import ImageProcessingFailedException
from google.api_core.exceptions import GoogleAPIError

class FrameAnalyzer:
    def __init__(self):
        """Initialize the FrameAnalyzer with the folder containing frames."""
        
        # Initialize the Google Cloud Vision API client
        self.client = vision.ImageAnnotatorClient()

    def __analyze_image(self, image_path):
        """Analyze an image using Google Cloud Vision API to extract tags."""
        
        # Read the image file
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        # Perform label detection on the image
        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        
        # Check for errors in the response
        labels = response.label_annotations
        if not labels:
            print(f"No labels found for image: {image_path}")
            return set()
        
        # Extract labels (tags) from the response
        tags = {label.description for label in labels}
        
        # Handle errors
        if response.error.message:
            raise ImageProcessingFailedException(f"{response.error.message}")
        
        return tags
    
    def analyze_all_frames(self, frames_folder):
        """Analyze all frames in the specified folder and return a set of tags."""
        
        try:
            tags = set()
            if not os.path.exists(frames_folder):
                raise FileNotFoundError(f"Frames folder not found: {frames_folder}")
            if not os.listdir(frames_folder):
                raise FileNotFoundError(f"No frames found in the folder: {frames_folder}")
            else:
                # Iterate through all files in the frames folder
                for filename in os.listdir(frames_folder):
                    image_path = os.path.join(frames_folder, filename)
                    sub_tags = self.__analyze_image(image_path)
                    tags = tags.union(sub_tags)
            
            print("successfully created Object tags")
            # Return the tags for all frames
            return tags
        
        except (FileNotFoundError, PermissionError, OSError) as e:  
            raise FramesProcessingFailedException(f" Failed to access {frames_folder}", errors=str(e))
        except (GoogleAPIError, ImageProcessingFailedException) as e:
            raise FramesProcessingFailedException(f"Google API error: {str(e)}")        
        except Exception as e:
            print(f"Error analyzing frames: {e}")
            
        

