from GooBa import Document, Element

# Initialize Document and Router
doc = Document()

h1 = Element("h1")
h1.text = "Hello World"

doc.body(h1)
doc.build()
