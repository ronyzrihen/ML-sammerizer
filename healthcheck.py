import sys
from requests import get, exceptions

try:
    response = get("http://localhost:8000/healthcheck", timeout=2)
    if response.ok:
        print("Healthcheck successful.")
        sys.exit(0)
    print(f"Healthcheck failed with status: {response.status_code}")
    sys.exit(1)
except exceptions.RequestException as e:
    print(f"Healthcheck failed with error: {e}")
    sys.exit(1)
