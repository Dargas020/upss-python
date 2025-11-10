# UPSS — Secure Communication Protocol Library for Python

**UPSS** is a lightweight, security-first Python library implementing the **UPSS protocol** — a custom communication protocol designed with **end-to-end encryption**, secure session handling, and structured message exchange over TCP sockets.

Built for developers who prioritize **data confidentiality** and **integrity**, UPSS abstracts low-level socket programming while enforcing cryptographic best practices out of the box.

---

## 🔐 Key Features

- **Mandatory encryption**: All payloads are encrypted using symmetric cryptography (`cryptography`).
- **Route-based request handling**: Decorator-style endpoint registration.
- **Structured data model**: Messages are encapsulated in typed `Package` objects with status, type, and payload.
- **Client & server utilities**: Full-stack support with minimal boilerplate.

---

## 🚀 Quick Start

### Installation

```bash
pip install upss-py
```
### Server Example

```python
from upss import UPSS
from upss.models import Status
from upss.security import cryptographer

app = UPSS(
    addr="localhost",
    port=1234,
    encoding="utf-8"
)


# Example handle "/" 
@app.url("/")
def auth_handler(client, encoding, key, data):
    print(cryptographer.decrypt_data(data["msg"], encoding, key))  # Hello Server!!!
    return Status.ok  # Return OK


if __name__ == "__main__":
    app.run()
```
### Client Example

```python
from cryptography.fernet import Fernet
from upss import client
from upss.models import Package, Types
from upss.security import cryptographer

key = Fernet.generate_key()

data = {
    "msg": cryptographer.encrypt_data("Hello Server!!!", "utf-8", key)
}

# Connect to "/"
for connection in client.connect("upss://localhost:1234", encoding="utf-8", key=key):
    connection.send(Package("/", Types.SEND, data))  # Send `Hello Server!!!`
    print(connection.get())  # Server said: OK
```

## 🔒 Security Model
Symmetric encryption only: keys are automatically transmitted via a handshake. The protocol requires constant updating of encryption keys.
Plaintext is not allowed: the protocol assumes that all data fields are encrypted;
