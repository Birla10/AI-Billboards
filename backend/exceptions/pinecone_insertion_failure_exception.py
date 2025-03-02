class PineconeInsertionFailureException(Exception):
    def __init__(self, message="Failed to insert data into Pinecone"):
        self.message = message
        super().__init__(self.message)