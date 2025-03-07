import os
from dotenv import load_dotenv

import cv2
import torch
import clip
import numpy as np
from PIL import Image
from openai import OpenAI
from openai import OpenAIError

from exceptions.embeddings_generation_failed_exception import EmbeddingsGenerationFailedException

class CreateEmbeddings:
    
    def __init__(self, model_name='ViT-B/32', device='cuda' if torch.cuda.is_available() else 'cpu', frame_skip=5):
        """
        Initialize the CLIP model and preprocessing pipeline.
        :param model_name: CLIP model variant (e.g., 'ViT-B/32', 'ViT-L/14')
        :param device: 'cuda' if GPU is available, else 'cpu'
        :param frame_skip: Number of frames to skip (higher = fewer frames)
        """
        
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.frame_skip = frame_skip  # Process every nth frame

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
    
    def create_context_embeddings(self, video_path):
        """
        Create a single video embedding by averaging frame embeddings.
        :param video_path: Path to the video file.  
        :return: The averaged CLIP embedding of the video.
        """
        try:
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
        
            if not frame_embeddings:
                print("No valid embeddings extracted!")
                return None
        
            return np.mean(frame_embeddings, axis=0).tolist()
            
        except (FileNotFoundError, ValueError) as e:
            raise EmbeddingsGenerationFailedException("Invalid video path or format", errors=str(e))
        except (KeyError, IndexError, AttributeError) as e:
            raise EmbeddingsGenerationFailedException("Invalid response received", errors=str(e))
        except (OpenAIError, ConnectionError, TimeoutError, ValueError) as e:
            raise EmbeddingsGenerationFailedException("Failed to generate embeddings", errors=str(e))
        except Exception as e: 
            raise EmbeddingsGenerationFailedException("An unexpected error occurred", errors=str(e))
            
    
    def create_obj_embeddings(self, object_tags):
        
        try:
            print("inside createing embeddings")
              
            response = self.client.embeddings.create(
                input = object_tags,
                dimensions=512,
                model = "text-embedding-3-small",
                encoding_format="float"
            )
        
            if response:
                print(f"successfully created embeddings")
            else:
                print(f"Failed to create embeddings")
        
            embeddings_list = [embedding.embedding for embedding in response.data]  # List of embeddings

            # If multiple tags exist, take the average embedding
            return np.mean(embeddings_list, axis=0).tolist()  # Ensures 1536-dimension

        except (KeyError, IndexError, AttributeError) as e:
            raise EmbeddingsGenerationFailedException("Invalid response received", str(e))
        except (OpenAIError, ConnectionError, TimeoutError, ValueError) as e:
            raise EmbeddingsGenerationFailedException("Failed to generate embeddings", str(e))
        except Exception as e:
            raise EmbeddingsGenerationFailedException("An unexpected error occurred", str(e))
            

        
        