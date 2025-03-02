class FirebaseUploadFailedException(Exception):
    def __init__(self, message="Failed to upload to Firebase", errors=None):
        super().__init__(message)
        self.errors = errors