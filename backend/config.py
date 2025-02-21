import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage, firestore
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()
# Get the JSON key path
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Set the environment variable dynamically
if google_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
else:
    raise Exception("GOOGLE_APPLICATION_CREDENTIALS is not set in the .env file!")


# Initialize Firebase App only once
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET') 
    })
        
    # Get storage bucket reference
    firebase_bucket = storage.bucket()
    ai_billboards_db = firestore.client(database_id=os.getenv('FIRESTORE_DATABASE_ID'))
    
pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

client = OpenAI(api_key="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")