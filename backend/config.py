import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

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
        'storageBucket': 'ai-billboards-63f04.appspot.com' 
    })
        
    # Get storage bucket reference
    firebase_bucket = storage.bucket()

