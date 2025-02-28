from data_fetching.weather import WeatherService
from data_fetching.currentTime import TimeClassifier
from ai_analysis.emotion_detection import get_emotion
from ai_analysis.create_embeddings import CreateEmbeddings
from database.pinecone_similarity_search import SimilaritySearch

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
        query = get_emotion() + " " + "person in "  + weather.get_weather() + " " + current_time.get_month() + " " + current_time.get_time_period()

        print(query)
        
        # Create embeddings for the query
        create_embeddings = CreateEmbeddings()
        query_embeddings = create_embeddings.create_obj_embeddings(query)
        
        similaritySearch = SimilaritySearch()
        
        # Perform similarity search
        return similaritySearch.perform_similarity_search(query_embeddings)