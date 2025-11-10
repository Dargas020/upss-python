from datetime import datetime


def i(q: str, x: object):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"INFO:\t{timestamp} — \"{q}\" {str(x)}")


def w(q: str, x: object):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[33mINFO:\t{timestamp} — \"{q}\" {str(x)}\033[0m")


def e(q: str, x: object):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[31mERROR:\t{timestamp} — \"{q}\" {str(x)}\033[0m")
