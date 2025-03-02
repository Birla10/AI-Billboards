class FramesExtractionFailedException(Exception):
    def __init__(self, message="Failed to extract frames from the video"):
        self.message = message
        super().__init__(self.message)