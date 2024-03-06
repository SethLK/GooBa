from component.plane import Document
from component.HTMLElement import HTMLElement

h1 = HTMLElement("h1")
h1.set_text("HELlo")

doc = Document()
doc.body(h1)
doc.build()