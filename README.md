Here's a small README for your project:

---

# BotOps Client

**BotOps** is a Python client library for interacting with the BotOps API. It provides an easy-to-use interface for managing databases, sending chat requests, and performing health checks through the BotOps REST API.

---

## Features

- Manage databases (list, create, update, delete).
- Send chat requests to the BotOps API.
- Perform health checks on the API server.
- Supports flexible filtering with a syntax similar to PocketBase.
- Extensible design for adding new API endpoints.

---

## Installation

You can install the library via pip:

```bash
pip install botops
```

Or from source:

```bash
git clone https://github.com/ArnauCosta/BotopsClient.git
cd BotopsClient
pip install .
```

---

## Usage

### Initialize the Client
```python
from botops import BotOps

# Initialize the client
botops = BotOps(base_url="http://your-api-url")
```

### Working with Databases
#### List All Databases
```python
databases = botops.database.list()
for db in databases:
    print(db.name)
```

#### List Databases with Filters
```python
filtered_dbs = botops.database.list(filters='name~"Test" AND created_at>="2024-01-01T00:00:00"')
for db in filtered_dbs:
    print(db.name)
```

#### Apply a Function to Each Database
```python
def print_database(db):
    print(f"Database Name: {db.name}")

botops.database.for_each(print_database, filters='name~"Test"')
```

#### Create a New Database
```python
from botops.client import Database, Attribute

new_db = Database(
    name="TestDB",
    created_at="2024-11-29T00:00:00",
    attributes=[Attribute(attribute="id", type="int")]
)
created_db = botops.database.create(new_db)
print(created_db.id)
```

### Send Chat Requests
```python
from botops.client import ChatRequest

chat_request = ChatRequest(prompt="Hello, AI!")
response = botops.chat.send(chat_request)
print(response)
```

### Health Check
```python
health = botops.health.check()
print("API Health:", health)
```

---

## Dependencies

- Python 3.7+
- `requests`
- `pydantic`

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you'd like to change.

---

## Author

Created by **Arnau Costa**.  
Email: [arnaucosta23@gmail.com](mailto:arnaucosta23@gmail.com)  
GitHub: [https://github.com/ArnauCosta](https://github.com/ArnauCosta)

---
