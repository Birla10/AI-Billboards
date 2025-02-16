from google.cloud import vision
import os
from dotenv import load_dotenv

class FrameAnalyzer:
    def __init__(self, frames_folder="frames"):
        """Initialize the FrameAnalyzer with the folder containing frames."""
        
        # Set the path to the frames folder
        self.frames_folder = frames_folder
        
        # Initialize the Google Cloud Vision API client
        self.client = vision.ImageAnnotatorClient()

    def analyze_image(self, image_path):
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
            return []
        
        # Extract labels (tags) from the response
        tags = [label.description for label in labels]
        
        # Handle errors
        if response.error.message:
            raise Exception(f"{response.error.message}")
        
        # Print the tags
        print(f"Image: {image_path}, Tags: {tags}")
        return tags

    def analyze_all_frames(self):
        if not os.path.exists(self.frames_folder):
            print(f"Frames folder '{self.frames_folder}' does not exist.")
        else:
            # Iterate through all files in the frames folder
            for filename in os.listdir(self.frames_folder):
                image_path = os.path.join(self.frames_folder, filename)
                self.analyze_image(image_path)

