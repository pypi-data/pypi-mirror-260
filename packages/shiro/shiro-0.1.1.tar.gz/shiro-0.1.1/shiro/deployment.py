class Deployment:
    def __init__(self, client):
        self.client = client

    def list(self):
        """List all deployments."""
        return self.client.request("GET", "deployments")

    def retrieve(self, deployment_id):
        """Retrieve a specific deployment by its ID."""
        return self.client.request("GET", f"deployments/{deployment_id}")

    def update(self, deployment_id, data):
        """Update a specific deployment."""
        return self.client.request("PATCH", f"deployments/{deployment_id}", data)
