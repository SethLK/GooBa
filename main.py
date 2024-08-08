from GooBa import Document, Element

doc = Document()
div = Element("div")

h1 = Element("h1")
h1.text = "Hello ld"

div.appendChild(h1)

h1.text = "Hello There"

div.appendChild(h1)

doc.body(div)
doc.build()
