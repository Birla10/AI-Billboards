from pinecone import ServerlessSpec
from config import pinecone
import os
from dotenv import load_dotenv

class InsertEmbeddings:
    
    def __init__(self):
      
      load_dotenv()
      self.context_embeddings_host = os.getenv("PINECONE_CONTEXT_EMBEDDINGS_INDEX_HOST") 
        
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
    
    def insert_obj_embeddings(self, embeddings, index_name):
        
        if pinecone.has_index(index_name):
            
            index = pinecone.Index(host=self.context_embeddings_host)
            
            upsert_response = index.upsert(
                vectors=[
                    {
                        "id": "vec1",
                        "values": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                        "sparse_values": {
                            "indices": [1, 5],
                            "values": [0.5, 0.5]
                        },
                        "metadata": {
                            "genre": "drama"
                        }
                    }
                ],
                namespace="example-namespace"
            )   
            
            