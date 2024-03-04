import requests

from marcsync.collection import Collection


class MarcSync:

    def __init__(self, access_token: str):
        self.accessToken = access_token

    def get_collection(self, collection_name: str):
        return Collection(self.accessToken, collection_name)

    def fetch_collection(self, collection_name: str):
        result = requests.get("https://api.marcsync.dev/v0/collection/" + collection_name,
                              headers={"Authorization": self.accessToken})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 404:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        return Collection(self.accessToken, collection_name)

    def create_collection(self, collection_name: str):
        result = requests.post("https://api.marcsync.dev/v0/collection/" + collection_name,
                               headers={"Authorization": self.accessToken})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection already exists")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        return Collection(self.accessToken, collection_name)
