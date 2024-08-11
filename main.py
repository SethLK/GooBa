from GooBa import Document, Element

# Create a new document
doc = Document()

# Create elements
div = Element("div", id="main-div")
div.style = {
    "background-color": "red"
}

h1 = Element("h1")
h1.text = "Hello ld"

h1.style = {
    "color": "#00ff00",
}

div.appendChild(h1)

h1_2 = Element("h1")
h1_2.text = "Hello There"

div.appendChild(h1_2)

# Add elements to the document
doc.body(div)

# Build the document
doc.build()
