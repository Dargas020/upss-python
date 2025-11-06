import json
import random
import string
from datetime import datetime

from upss.models import Package, URL
from upss.exception import URLError


def generate_package(package_str):
    package_json = json.loads(package_str)
    return Package(package_json["path"], package_json["type"], package_json["data"])


def generate_url(url: str):
    try:
        parts_1 = url.split("://")
        protocol = parts_1[0]
        parts_2 = parts_1[1].split(":")
        addr = parts_2[0]
        if "/" in parts_2[1]:
            parts_3 = parts_2[1].split("/", maxsplit=1)
            port, path = parts_3
            return URL(protocol, addr, int(port), "/" + path)
        else:
            port = parts_2[1]
            return URL(protocol, addr, int(port), "/")
    except Exception as e:
        raise URLError(f"There is an error in the URL format. '{url}'")


def generate_token():
    length = 32
    all_symbols = string.ascii_lowercase + string.digits
    now = datetime.now()
    result = (now.strftime("%Y%m%d%H%M%S") +
              "".join(random.choice(string.ascii_uppercase) for _ in range(17)))
    for i in range(3):
        result += "."
        result += "".join(random.choice(all_symbols) for _ in range(length))
    return result
