# AndromedaClient

AndromedaClient is a python client for interacting with the Andromeda API of the Rhine-Neckar Metropolitan Region.

## Installation

You can install AndromedaClient using pip:

```bash
pip install andromedaClient
```

## Usage

First, import the AndromedaClient class and create a new client:

```python
from andromedaClient import AndromedaClient
# username and password is only required for upload operations
client = AndromedaClient('https://contextbroker.digitale-mrn.de', 'username', 'password')
```

You can then use the client to make requests to the Andromeda API:

```python
response = client.get('/entities/?type=Gemeinde')
```
