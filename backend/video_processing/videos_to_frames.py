import cv2
import os
from pathlib import Path

def extract_frames(video_path, frame_rate=1):
    """Extract frames from a video file and save them as images."""
    
    output_folder = f"resources/frames/{Path(video_path).stem}/"
    
    # Check if the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if video_path is None:
        raise ValueError("No video path provided.")
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise Exception(f"Could not open video file {video_path}")
    
    # Get the frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Calculate the interval for frame extraction
    frame_interval = int(fps / frame_rate)  # Extract 1 frame per second

    # Loop through the video and save frames
    frame_count = 0
    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If the frame is not read correctly, break the loop
        if not ret:
            break
        
        # Save the frame if it matches the interval
        if frame_count % frame_interval == 0:
            
            # Construct the output file path
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            
            # Save the frame as an image
            cv2.imwrite(frame_path, frame)
            
        # Increment the frame count
        frame_count += 1

    # Release the video capture object
    cap.release()
    print(f"Frames saved in {output_folder}")
