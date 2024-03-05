class Prompt:
    def __init__(self, client):
        self.client = client

    def list(self):
        """List all prompts."""
        return self.client.request("GET", "prompts")

    def retrieve(self, prompt_id):
        """Retrieve a specific prompt by its ID."""
        return self.client.request("GET", f"prompts/{prompt_id}")
