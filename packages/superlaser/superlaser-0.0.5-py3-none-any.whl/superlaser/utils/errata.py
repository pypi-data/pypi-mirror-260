class ApiKeyError(Exception):
    """
    Raised when API key is not provided.
    """

    def __init__(self):
        super().__init__(
            "API key not provided. Please set the RUNPOD_API_KEY environment variable for proper API security."
        )
