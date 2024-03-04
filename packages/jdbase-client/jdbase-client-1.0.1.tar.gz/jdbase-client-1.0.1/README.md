# jdbase

jdbase-client is a ORM for JDBase

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)


## Introduction

`jdbase-client` is a Python library designed to provide a convenient interface for interacting with JDBase remote database via an HTTP API. It simplifies common database operations such as creating, reading, updating, and deleting records, as well as performing custom queries. This library assumes that a compatible server is running and accessible at the provided API endpoin
## Installation

To install jdbase-client, simply use pip:

```bash
pip install jdbase-client
```

## Usage

```python
from jdbase_client import Database

# Configuration settings
config = {
    'api_key': 'adminkey',
    'api_endpoint': 'http://127.0.0.1:5000/api',
    'db': 'db2'
}

# Instantiate the Database object
db = Database(config)

# Example usage: Matching records
matching_records = db.match({"id": 2, "age": 30})
print(matching_records)
```

For More Read Docs [HERE](https://rakibmia7254.github.io/jdbase-client/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.