import requests


class Entry:
    def __init__(self, access_token: str, collection_name: str, data: dict):
        self.accessToken = access_token
        self.collectionName = collection_name
        self.data = data

    def get_values(self):
        return self.data.items()

    def get_value(self, key: str):
        return self.data.get(key)

    def get_collection_name(self):
        return self.collectionName

    def update_value(self, key: str, value: str):

        if key == "_id":
            raise Exception("Cannot update _id")

        result = requests.put("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": {"_id": self.data.get("_id")}, "data": {key: value}})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        self.data[key] = value

    def update_values(self, values: dict):

        if "_id" in values:
            raise Exception("Cannot update _id")

        result = requests.put("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                              headers={"Authorization": self.accessToken},
                              json={"filters": {"_id": self.data.get("_id")}, "data": values})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")

        self.data.update(values)

    def delete(self):
        result = requests.delete("https://api.marcsync.dev/v1/entries/" + self.collectionName,
                                 headers={"Authorization": self.accessToken},
                                 json={"filters": {"_id": self.data.get("_id")}})
        if result.status_code == 401:
            raise Exception("Invalid access token")
        if result.status_code == 400:
            raise Exception("Entry not found")
        if result.status_code == 429:
            raise Exception("Rate limit exceeded")
