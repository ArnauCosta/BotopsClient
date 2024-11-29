import requests
from pydantic import BaseModel
from typing import List, Optional


class Attribute(BaseModel):
    attribute: str
    type: str


class Database(BaseModel):
    name: str
    created_at: str
    attributes: List[Attribute]


class DatabaseOut(Database):
    id: str


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    model: str = "llama3.1"
    provider: str = "ollama"
    api_base: str = "http://ollama:11434"
    api_key: str = ""
    stream: bool = True


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def get(self, endpoint: str, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json=None):
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json=None):
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str):
        return self._request("DELETE", endpoint)


class DatabaseAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def list(self, filters: Optional[str] = None) -> List[DatabaseOut]:
        """
        Retrieve a list of databases with optional filters.

        Args:
            filters (str, optional): A filter string following the syntax:
                                     OPERAND OPERATOR OPERAND (e.g., "name~test").
                                     Multiple filters can be joined with AND/OR.

        Returns:
            List[DatabaseOut]: A list of databases matching the filter criteria.
        """
        params = {}
        if filters:
            params["filters"] = filters
        response = self.client.get("/api/database/", params=params)
        return [DatabaseOut(**db) for db in response]

    def create(self, database: Database) -> DatabaseOut:
        response = self.client.post("/api/database/", json=database.dict())
        return DatabaseOut(**response)

    def get(self, database_id: str) -> DatabaseOut:
        response = self.client.get(f"/api/database/{database_id}")
        return DatabaseOut(**response)

    def update(self, database_id: str, database: Database) -> DatabaseOut:
        response = self.client.put(f"/api/database/{database_id}", json=database.dict())
        return DatabaseOut(**response)

    def delete(self, database_id: str):
        self.client.delete(f"/api/database/{database_id}")

    def for_each(self, func: callable, filters: Optional[str] = None):
        """
        Apply a function to each database that matches the filter.

        Args:
            func (callable): A function that takes a single DatabaseOut object as input.
            filters (str, optional): A filter string to filter databases before applying the function.

        Example:
            def print_db_name(db):
                print(db.name)

            db_api.for_each(print_db_name, filters="name~Test")
        """
        databases = self.list(filters=filters)
        for db in databases:
            func(db)



class ChatAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def send(self, chat_request: ChatRequest):
        return self.client.post("/api/chat", json=chat_request.dict())


class HealthAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def check(self):
        return self.client.get("/api/health")


class BotOps:
    def __init__(self, base_url: str):
        self.client = APIClient(base_url)
        self.database = DatabaseAPI(self.client)
        self.chat = ChatAPI(self.client)
        self.health = HealthAPI(self.client)

    def add_api(self, name: str, api_class):
        setattr(self, name, api_class(self.client))


if __name__ == "__main__":

    botops = BotOps(base_url="http://localhost")

    # db = botops.database
    # new_db = Database(
    #     name="TestDB",
    #     created_at="2024-11-29T00:00:00",
    #     attributes=[Attribute(attribute="id", type="int")],
    # )
    # created_db = db.create(new_db)
    # print(created_db)

    def print_database_name(db: DatabaseOut):
        print(f"Database Name: {db.name}, Created At: {db.created_at}")

    botops.database.for_each(print_database_name, filters='name~"Test" AND created_at>="2024-01-01T00:00:00"')


    # chat = botops.chat
    # chat_request = ChatRequest(prompt="Hello")
    # chat_response = chat.send(chat_request)
    # print(chat_response)

    # health = botops.health
    # health_status = health.check()
    # print(health_status)
