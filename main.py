from component.parent import Parent
from component.Document import Document
from component.HTMLElement import HTMLElement

doc = Document()

doc.title("Testing")

parent = Parent("div")

child_h1 = HTMLElement("h1")
child_h1.text = "HEllo There"

parent.add_child(child_h1)

doc.body(parent)

doc.build()
