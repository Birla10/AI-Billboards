class FramesProcessingFailedException(Exception):
    def __init__(self, message="Failed to process frames", errors=None):
        super().__init__(message)
        self.errors = errors