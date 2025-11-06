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
from upss.security import cryptographer

app = UPSS(
    addr="localhost",
    port=1234,
    encoding="utf-8",
    crypto=cryptographer.generate_crypto()
)


# Example handle "/" 
@app.url("/")
def auth_handler(client_sock, encoding, key, data):
    print(cryptographer.decrypt_data(data["msg"], encoding, key))  # Hello Server!!!
    pass


if __name__ == "__main__":
    app.run()
```
### Client Example

```python
from upss import client
from upss.security import cryptographer
from cryptography.fernet import Fernet

key = Fernet.generate_key()

data = {
    "msg": cryptographer.encrypt_data("Hello Server!!!", "utf-8", key)
}

# Connect to "/"
client.connect("upss://localhost:1234", encoding="utf-8", send_data=data, key=key)
```

## 🔒 Security Model
Symmetric encryption only: keys are automatically transmitted via a handshake. The protocol requires constant updating of encryption keys.
Plaintext is not allowed: the protocol assumes that all data fields are encrypted;
