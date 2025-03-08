import os
import tensorflow as tf
import warnings
from dotenv import load_dotenv

load_dotenv()
# Get the JSON key path
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Set the environment variable dynamically
if google_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
else:
    raise Exception("GOOGLE_APPLICATION_CREDENTIALS is not set in the .env file!")
    
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'

tf.get_logger().setLevel('ERROR')
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
