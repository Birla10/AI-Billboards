class FileSaveErrorException(Exception):
    """Exception raised for errors in the file saving process."""

    def __init__(self, message="Error occurred while saving the file"):
        self.message = message
        super().__init__(self.message)