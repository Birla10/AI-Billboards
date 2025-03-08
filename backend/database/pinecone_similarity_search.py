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
        context_ids = self.__search_context_index(self.context_index_name, query)

        obj_ids = self.__search_object_index(self.object_index_name, query)
        
        common_ids = set()
        
        for obj_id in obj_ids:
            obj_id_prefix = obj_id.split('_')[0]
            for context_id in context_ids:
                context_id_prefix = context_id.split('_')[0]
                if obj_id_prefix == context_id_prefix:
                    common_ids.add(obj_id_prefix)
        
        return common_ids
                   
    def __search_context_index(self, index_name, query):
        
        print(f"searching index {index_name}")
        
        # Connect to the index
        index = self.pinecone.Index(index_name)
        
        # Perform the query
        query_results = index.query(
            vector=query,
            top_k=3,
            include_metadata=True
        )
        
        context_index_ids = {}
        # Print the results        
        for match in query_results.matches:
            context_index_ids[match.id] = match.metadata.get("video_url")
            
        return context_index_ids
    
    def __search_object_index(self, index_name, query):
        
        print(f"searching index {index_name}")
        
        # Connect to the index
        index = self.pinecone.Index(index_name)
        
        # Perform the query
        query_results = index.query(
            vector=query,
            top_k=3,
            include_metadata=True
        )
        
        obj_index_ids = {}
        # Print the results        
        for match in query_results.matches:
            obj_index_ids[match.id] = match.metadata.get("video_url")
            
        return obj_index_ids
