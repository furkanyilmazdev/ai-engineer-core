class InvalidDataFormatError(Exception):
    """Veri formatı AI modeline uygun olmadığında fırlatılır."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)