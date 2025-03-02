import os
from pathlib import Path
from dotenv import load_dotenv

from pinecone import ServerlessSpec
from config import pinecone
from openai import OpenAIError

from exceptions.pinecone_insertion_failure_exception import PineconeInsertionFailureException

class InsertEmbeddings:
    
    def __init__(self):
      
      load_dotenv()
      self.object_index_name = os.getenv("PINECONE_OBJECT_INDEX")
      self.context_index_name = os.getenv("PINECONE_CONTEXT_INDEX")
      
      self.object_index_exists = pinecone.has_index(self.object_index_name)
      self.context_index_exists = pinecone.has_index(self.context_index_name)
      
      if not self.object_index_exists:
          print(self.object_index_name)
          self.__create_index(self.object_index_name)
          self.object_index_exists = True
        
      if not self.context_index_exists:
          print(self.context_index_name)
          self.__create_index(self.context_index_name)   
          self.context_index_exists = True   
          
      self.context_embeddings_host = os.getenv("PINECONE_CONTEXT_EMBEDDINGS_INDEX_HOST") 
      self.object_embeddings_host = os.getenv("PINECONE_OBJECT_EMBEDDINGS_INDEX_HOST")    
        
    def __create_index(self, index_name):
        """
            Insert the embeddings into Pinecone.
        """
        try:
            print(f"creating index {index_name}")
        
            pinecone.create_index(
                name=index_name,
                dimension=512,
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

            index_desc = pinecone.describe_index(index_name)
            os.environ["PINECONE_OBJECT_EMBEDDINGS_INDEX_HOST"] = index_desc.host
            print("Pinecone index created successfully.") 
        
        except (KeyError, IndexError, AttributeError) as e:
             raise PineconeInsertionFailureException("Failed to create index", errors=str(e)) 
        except (OpenAIError, ConnectionError, TimeoutError, ValueError) as e:
            raise PineconeInsertionFailureException("Failed to create index", errors=str(e))
        except Exception as e:
            raise PineconeInsertionFailureException("An unexpected error occurred", errors=str(e))
            
    def insert_to_pinecone(self, embeddings:list, tags:list, storage_url:str, tag_type:str):
        """
            Insert the embeddings into Pinecone.
        """
        try:
            print("inserting to pinecone")
            if tag_type == "obj":
                index_id = Path(storage_url).stem + "_object"
                host_id = self.object_embeddings_host
            else:
                index_id = Path(storage_url).stem + "_context"
                host_id = self.context_embeddings_host
            
            index = pinecone.Index(host=host_id)
            upsert_response = index.upsert(
                vectors=[
                    {
                        "id": index_id,
                        "values": embeddings,
                        "metadata": {
                            "tags": tags,
                            "video_url": storage_url
                        }
                    }
                ]
            )  
        
            if upsert_response:
                print(upsert_response)
        
        except (KeyError, IndexError, AttributeError) as e:
            raise PineconeInsertionFailureException("Invalid response received", errors=str(e))
        except (OpenAIError, ConnectionError, TimeoutError, ValueError) as e:
            raise PineconeInsertionFailureException("Failed to insert embeddings", errors=str(e))
        except Exception as e:
            raise PineconeInsertionFailureException("An unexpected error occurred", errors=str(e))
            
 
            
       