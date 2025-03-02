class EmbeddingsGenerationFailedException(Exception):
    def __init__(self, message="Failed to generate embeddings"):
        self.message = message
        super().__init__(self.message)