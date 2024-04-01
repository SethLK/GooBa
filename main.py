from component.HTMLElement import HTMLElement
from component.Document import Document
from component.parent import Parent
import requests

doc = Document()
root = Parent("div")

h1 = HTMLElement("h1")

try:
    res = requests.get("https://jsonplaceholder.typicode.com/todos")
    data = res.json()
    for i in range(5):
        h1.text = data[i]["title"]
        root.add_child(h1)


except requests.exceptions.RequestException as e:
    print("Error:", e)

doc.body(root)
doc.build()
