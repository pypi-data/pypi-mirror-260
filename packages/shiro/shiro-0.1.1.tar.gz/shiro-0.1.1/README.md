# Shiro Python Library

This is the official [Shiro API](https://openshiro.com/api/v1/docs) Python library maintained by [OpenShiro](https://openshiro.com). The Shiro Python library provides convenient access to the Shiro API from applications written in the Python language.

## Documentation

See the [API docs](https://openshiro.com/api/v1/docs) and also this post on [Getting Started with the Shiro API](https://openshiro.com/docs/getting-started-with-the-shiro-api).

## Usage
The library needs to be configured with your account's api key which is available in your Shiro account under API Keys.

### Initialize the client with your API key
````
from shiro import ShiroClient

client = ShiroClient("your_api_key_here")
````

### List all deployments
````
deployments = client.deployments.list()
````

### Retrieve a specific deployment
````
deployment = client.deployments.retrieve("dpmt_lWokJnPAwQCeV2ZWovjG7BNr")
````

### Update a deployment
````
update_data = {"name": "Updated Deployment Name"}
updated_deployment = client.deployments.update("dpmt_lWokJnPAwQCeV2ZWovjG7BNr", update_data)
````

### List all prompts
````
prompts = client.prompts.list()
````

### Retrieve a specific prompt
````
prompt = client.prompts.retrieve("prmt_9nORYX8zAYHGo2AVQ1a2w03p")
````

### Create a new completion

````
completion_data = {
    "deployment_id": "dpmt_lWokJnPAwQCeV2ZWovjG7BNr",
    "prompt_id": "prmt_9nORYX8zAYHGo2AVQ1a2w03p",  # Optional
    "input_variables": {
        "review_text": "I loved the movie."
    }
}
completion = client.generate_completion.create(completion_data)
````

## Support

New features and bug fixes are released on the latest major version of the Shiro Python library. If you are on an older major version, we recommend that you upgrade to the latest in order to use the new features and bug fixes including those for security vulnerabilities. Older major versions of the package will continue to be available for use, but will not be receiving any updates.


## Development

Run all tests

````
python -m unittest discover tests
````
