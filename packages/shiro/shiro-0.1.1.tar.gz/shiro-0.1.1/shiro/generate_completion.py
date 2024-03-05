class GenerateCompletion:
    def __init__(self, client):
        self.client = client

    def create(self, data):
        """Create a new completion."""
        return self.client.request("POST", "generate_completion", data)
