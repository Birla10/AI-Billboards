import firebase_admin
from firebase_admin import credentials, storage
from config import firebase_bucket

class FirebaseUploader:
    def __init__(self):
        self.bucket = firebase_bucket

    def upload_video(self, video_path, make_public=False):
        """
        Uploads a video to Firebase Storage.

        :param video_path: Local path of the video file (e.g., 'local_videos/sample.mp4')
        :param make_public: If True, makes the file publicly accessible.
        :return: The public URL of the uploaded file (if public), otherwise signed URL.
        """
        destination_blob_name = self.bucket.name + '/videos/' + video_path.split('/')[-1]
        
        blob = self.bucket.blob(destination_blob_name)

        # Upload the file
        blob.upload_from_filename(video_path)
        print(f'File {video_path} uploaded to {destination_blob_name}.')

        # Otherwise, generate a signed URL (valid for 1 hour)
        signed_url = blob.generate_signed_url(expiration=3600)
        print(f'Signed URL (Valid for 1 hour): {signed_url}')
        return signed_url
