from data_fetching.weather import WeatherService
from data_fetching.currentTime import TimeClassifier
from ai_analysis.emotion_detection import get_emotion
from ai_analysis.create_embeddings import CreateEmbeddings
from database.pinecone_similarity_search import SimilaritySearch
from sklearn.decomposition import PCA
import numpy as np

class AdSearch:
    
    """
    This class is used to search for ads in the pinecone database
    """
    def getAccurateAd(self):
        
        """
        This function is used to get the accurate ad from the pinecone database
        """
        weather = WeatherService()
        current_time = TimeClassifier()
        
        # Get search query
        query = "Happy" + " " + "person in "  + weather.get_weather() + " " + current_time.get_month() + " " + current_time.get_time_period()

        print(query)
        
        # Create embeddings for the query
        create_embeddings = CreateEmbeddings()
        query_embeddings = create_embeddings.create_obj_embeddings(query)
        
        print(f"Final embedding shape: {len(query_embeddings)}")
        
        reduced_embeddings = self.__reduced_dimension(query_embeddings)
        
        print(f"Final embedding shape: {len(reduced_embeddings)}")
        
        similaritySearch = SimilaritySearch()
        
        # Perform similarity search
        #return similaritySearch.perform_similarity_search(query_embeddings)
    
    def __reduced_dimension(self, embeddings):
        
        embeddings_array = np.array(embeddings)
        
        pca = PCA(n_components=512)
        return pca.fit_transform(embeddings_array.reshape(1, -1))