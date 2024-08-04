from GooBa import Document, Parent, Element, Link

doc = Document()

root = Parent("div", id="root")

sidebar = Parent("div")
main = Parent("div")

head = Element("h1")
head.text = "Hello THere"

to_home = Link("/")
to_about = Link("/")

home_page = Element

root.appendChild(sidebar, main)

doc.build()

