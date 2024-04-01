# Static Site Generation

import requests

try:
    res = requests.get("https://jsonplaceholder.typicode.com/todos")
    data = res.json()
    print(data[2]["title"])

except requests.exceptions.RequestException as e:
    print("Error:", e)