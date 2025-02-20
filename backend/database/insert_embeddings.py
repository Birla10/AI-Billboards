from pinecone import ServerlessSpec
from config import pinecone
import os
from pathlib import Path
from dotenv import load_dotenv

class InsertEmbeddings:
    
    def __init__(self):
      
      load_dotenv()
      self.context_embeddings_host = os.getenv("PINECONE_CONTEXT_EMBEDDINGS_INDEX_HOST") 
      self.object_embeddings_host = os.getenv("PINECONE_OBJECT_EMBEDDINGS_INDEX_HOST")
      self.object_index_name = os.getenv("PINECONE_OBJECT_INDEX")
      self.context_index_name = os.getenv("PINECONE_CONTEXT_INDEX")
      
      self.object_index_exists = pinecone.has_index(self.object_index_name)
      self.context_index_exists = pinecone.has_index(self.context_index_name)
      
      if not self.object_index_exists:
          self.__create_index(self.object_index_name)
          self.object_index_exists = True
        
      if not self.context_index_exists:
          self.__create_index(self.context_index_name)   
          self.context_index_exists = True       
        
    def __create_index(self, index_name):
        """
            Insert the embeddings into Pinecone.
        """
        pinecone.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
            deletion_protection="enabled",
            tags={
                "environment": "development"
            }
        )
    
        print("Pinecone index created successfully.") 
    
    def __insert_obj_embeddings(self, embeddings, tags, url):
        
        if self.object_index_exists:          
            index = pinecone.Index(host=self.object_embeddings_host)
            upsert_response = index.upsert(
                vectors=[
                    {
                        "id": Path(url).stem + "_object",
                        "values": embeddings,
                        "metadata": {
                            "tags": tags,
                            "video_url": url
                        }
                    }
                ]
            )
            
    def __insert_context_embeddings(self, embeddings, tags, url):
        
        if self.context_index_exists:            
            index = pinecone.Index(host=self.context_embeddings_host)
            upsert_response = index.upsert(
                vectors=[
                    {
                        "id": Path(url).stem + "_context",
                        "values": embeddings,
                        "metadata": {
                            "tags": tags,
                            "video_url": url
                        }
                    }
                ]
            )  
            
    def insert_to_pinecone(self, obj_embeddings, obj_tags, context_embeddings, context_tags, storage_url):
        """
            Insert the embeddings into Pinecone.
        """
        self.__insert_obj_embeddings(obj_embeddings, obj_tags, storage_url)
        self.__insert_context_embeddings(context_embeddings, context_tags, storage_url)
       