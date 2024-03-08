from component.parent import Parent
from component.Document import Document
from component.HTMLElement import HTMLElement
from component.style import Style

doc = Document()
style = Style("#demo")

doc.title("Testing")

parent = Parent("div")

child_h1 = HTMLElement("h1", id="demo")
child_h1.text = "Hello There"

style.add_property("color", "red")

parent.add_child(child_h1)

h1 = HTMLElement("h1", class_name="demo")
h1.text = "HEllo H1"

h1_style = Style(".demo")
h1_style.add_property("color", "blue")
h1_style.add_property("background-color", "black")

doc.add_style(style, h1_style)

doc.body(parent, h1)

doc.build()
