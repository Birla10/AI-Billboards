class TagsGenerationFailedException(Exception):
    def __init__(self, message="Failed to generate tags"):
        self.message = message
        super().__init__(self.message)