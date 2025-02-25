import cv2
import torch
import clip
from PIL import Image
import numpy as np
from database.insert_embeddings import InsertEmbeddings 
from config import client

class CreateEmbeddings:
    
    def __init__(self, model_name='ViT-B/32', device='cuda' if torch.cuda.is_available() else 'cpu', frame_skip=5):
        """
        Initialize the CLIP model and preprocessing pipeline.
        :param model_name: CLIP model variant (e.g., 'ViT-B/32', 'ViT-L/14')
        :param device: 'cuda' if GPU is available, else 'cpu'
        :param frame_skip: Number of frames to skip (higher = fewer frames)
        """
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.frame_skip = frame_skip  # Process every nth frame
        self.insert_embeddings = InsertEmbeddings()

    def __process_frame(self, frame):
        """
        Process a single frame and extract its CLIP embedding.
        :param frame: The input frame (image) to process.   
        :return: The CLIP embedding of the frame.
        """
        
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)  # L2 Normalize
        
        return image_features.cpu().numpy().flatten()
    
    def create_context_embeddings(self, video_path, context_tags, storage_url):
        
        insert_embeds = InsertEmbeddings()
        cap = cv2.VideoCapture(video_path)
        frame_embeddings = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames to reduce redundant data
            if frame_count % self.frame_skip == 0:
                embedding = self.__process_frame(frame)
                frame_embeddings.append(embedding)

            frame_count += 1

        cap.release()
        
        self.insert_embeddings.insert_to_pinecone(frame_embeddings, context_tags, storage_url, "context")
        return np.array(frame_embeddings)  # Convert to NumPy array for efficient storage
    
    
    def create_obj_embeddings(self, object_tags:list, storage_url:str):
        """
        Create text embeddings for the tags using CLIP.
        :return: Dictionary of tags and their corresponding CLIP embeddings.
        """
        print("inside createing embeddings")
              
        response = client.embeddings.create(
            input = object_tags,
            model = "text-embedding-ada-002",
            encoding_format="float"
        )
        
        if response:
            print(f"successfully created embeddings for {storage_url}")
        else:
            print(f"Failed to create embeddings for {storage_url}")
        
        embeddings_list = [x for embedding in response.data for x in embedding.embedding]
        
        print(type(response.data))
        print(type(response.data[0]))
        print(type(response.data[0].embedding))
        print(response.data[0].embedding[:5])  # Print a few values

        self.insert_embeddings.insert_to_pinecone(embeddings_list, object_tags, storage_url, "obj")
        