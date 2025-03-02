class VideoProcessingFailedException(Exception):
    def __init__(self, message="Video processing failed", errors=None):
        super().__init__(message)
        self.errors = errors