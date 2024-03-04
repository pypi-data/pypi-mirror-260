import requests

from marcsync.entry import Entry


class Collection:

    def __init__(self, access_token: str, collection_name: str):
        self.accessToken = access_token
        self.collectionName = collection_name

    def drop(self):
        result = requests.delete("https://api.marcsync.dev/v0/collection/" + self.collectionName,
                                 headers={"Authorization": self.accessToken})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while dropping collection")

    def set_name(self, name: str):
        result = requests.put("https://api.marcsync.dev/v0/collection/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"collectionName": name})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while renaming collection")

        self.collectionName = name

    def get_name(self):
        return self.collectionName

    def exists(self):
        result = requests.get("https://api.marcsync.dev/v0/collection/" + self.collectionName,
                              headers={"Authorization": self.accessToken})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 404:
            return False
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while checking collection")

        return True

    def create_entry(self, data: dict):

        if "_id" in data:
            raise Exception("Cannot set _id while creating entry")

        result = requests.post("https://api.marcsync.dev/v0/entries/" + self.collectionName,
                               headers={"Authorization": self.accessToken},
                               json={"data": data})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while creating entry")

        data["_id"] = result.json().get("objectId")
        return Entry(self.accessToken, self.collectionName, data)

    def get_entry_by_id(self, entry_id: str):
        result = requests.get("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": {"_id": entry_id}})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 404:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while fetching entry")

        if len(result.json().get("entries")) == 0:
            raise Exception("Entry not found")

        return Entry(self.accessToken, self.collectionName, result.json().get("entries")[0])

    def get_entries(self, filters: dict = {}):
        result = requests.get("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": filters})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while fetching entries")

        return [Entry(self.accessToken, self.collectionName, entry) for entry in result.json().get("entries")]

    def delete_entry_by_id(self, entry_id: str):
        result = requests.delete("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                                 headers={"Authorization": self.accessToken},
                                 json={"filters": {"_id": entry_id}})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 404:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while deleting entry")

    def delete_entries(self, filters: dict = {}):
        result = requests.delete("https://api.marcsync.dev/v0/entries/" + self.collectionName,
                                 headers={"Authorization": self.accessToken},
                                 json={"filters": filters})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while deleting entries")

    def update_entry_by_id(self, entry_id: str, data: dict):

        if "_id" in data:
            raise Exception("Cannot update _id")

        result = requests.put("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": {"_id": entry_id}, "data": data})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 404:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while updating entry")

    def update_entries(self, data: dict, filters):

        if len(filters) == 0:
            raise Exception("Filters are required for updating entries.")

        if "_id" in data:
            raise Exception("Cannot update _id")

        result = requests.put("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": filters, "data": data})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Collection not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        if result.status_code != 200:
            raise Exception("Unknown error while updating entries")
