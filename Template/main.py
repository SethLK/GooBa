from GooBa import Document, CreateElement, CreateStyle

# Create a new document
doc = Document()

# Create elements
div = CreateElement("div", id="main-div")
div.style = {
    "background-color": "red"
}

h1 = CreateElement("h1")
h1.text = "Hello ld"

h1.style = {
    "color": "#00ff00",
}

div.appendChild(h1)

h1_2 = CreateElement("h1", className="h1")
h1_2.text = "Hello There"

div.appendChild(h1_2)

HomePage = CreateStyle()
HomePage.style(".h1", {
    "color": "blue",
})

doc.appendHead(HomePage)

doc.body(div)

doc.build()
