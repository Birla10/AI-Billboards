from pinecone import ServerlessSpec
from config import pinecone
import os
from pathlib import Path
from dotenv import load_dotenv

class SimilaritySearch:
    
    def __init__(self):

        load_dotenv()
        self.object_index_name = os.getenv("PINECONE_OBJECT_INDEX")
        self.context_index_name = os.getenv("PINECONE_CONTEXT_INDEX")
      
        self.context_embeddings_host = os.getenv("PINECONE_CONTEXT_EMBEDDINGS_INDEX_HOST") 
        self.object_embeddings_host = os.getenv("PINECONE_OBJECT_EMBEDDINGS_INDEX_HOST")  
      
    def perform_similarity_search(self, query):
        
        # Perform similarity search in the context index
        return self.__search_context_index(self.object_index_name, query)
        
    def __search_context_index(self, index_name, query):
        
        print(f"searching index {index_name}")
        
        # Connect to the index
        index = pinecone.Index(index_name)
        
        # Perform the query
        query_results = index.query(
            vector=query,
            top_k=3,
            include_metadata=True
        )
        
        # Print the results        
        for match in query_results.matches:
            print(f"ID: {match.id}, Score: {match.score}, Metadata: {match.metadata}")
