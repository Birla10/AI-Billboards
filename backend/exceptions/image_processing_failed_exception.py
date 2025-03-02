class ImageProcessingFailedException(Exception):
    def __init__(self, message="Image processing failed", errors=None):
        super().__init__(message)
        self.errors = errors