import requests

res = requests.get("https://jsonplaceholder.typicode.com/todos")
data = res.json()

print(data[1]["title"])