from component.parent import Parent
from component.Document import Document
from component.HTMLElement import HTMLElement
from component.style import Style

doc = Document()
style = Style("#demo")

doc.title("Testing")

parent = Parent("div")

home_ = HTMLElement("a", href="/")
home_.text = "Home"

google = HTMLElement("a", href="https://www.google.com")
google.text = "Google"

parent.add_child(home_, google)

doc.body(parent)

doc.build()
