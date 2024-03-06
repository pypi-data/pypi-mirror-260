import requests

from ..utils.env import env_with_fallback
from .credentials import get_client_credentials


class HashboardAPI:
    def __init__(self):
        self.base_uri = (
            env_with_fallback("HASHQUERY_API_BASE_URI", "HASHBOARD_CLI_BASE_URI")
            or "https://hashboard.com"
        )
        self.credentials = get_client_credentials()

    @property
    def project_id(self):
        return self.credentials.project_id

    def post(self, route: str, payload: dict):
        response = requests.post(
            f"{self.base_uri}/{route}",
            json=payload,
            headers=self.credentials.get_headers(),
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}. Response:\n"
                + response.text
            )

    def graphql(self, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        return self.post("graphql/", payload)
