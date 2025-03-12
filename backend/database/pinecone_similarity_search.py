import os
from dotenv import load_dotenv

from pinecone import Pinecone

class SimilaritySearch:
    
    def __init__(self):

        load_dotenv()
        self.object_index_name = os.getenv("PINECONE_OBJECT_INDEX")
        self.context_index_name = os.getenv("PINECONE_CONTEXT_INDEX")
      
        self.context_embeddings_host = os.getenv("PINECONE_CONTEXT_EMBEDDINGS_INDEX_HOST") 
        self.object_embeddings_host = os.getenv("PINECONE_OBJECT_EMBEDDINGS_INDEX_HOST")  
        
        self.pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
      
    def perform_similarity_search(self, query):
        
        # Perform similarity search in the context index
        context_id = self.__search_context_index(self.context_index_name, query)
    
        obj_id = self.__search_object_index(self.object_index_name, query)
        
        return [context_id.split('_')[0], obj_id.split('_')[0]]
                   
    def __search_context_index(self, index_name, query):
        
        print(f"searching index {index_name}")
        
        # Connect to the index
        index = self.pinecone.Index(index_name)
        
        # Perform the query
        query_results = index.query(
            vector=query,
            top_k=1,
            include_metadata=True
        )
        
        if query_results.matches:
            return query_results.matches[0].id
        else:
            return None
    
    def __search_object_index(self, index_name, query):
        
        print(f"searching index {index_name}")
        
        # Connect to the index
        index = self.pinecone.Index(index_name)
        
        # Perform the query
        query_results = index.query(
            vector=query,
            top_k=1,
            include_metadata=True
        )
        
        if query_results.matches:
            return query_results.matches[0].id
        else:
            return None
            
    
