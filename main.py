from component.parent import Parent
from component.Document import Document
from component.HTMLElement import HTMLElement
from component.style import Style
from router.route import Route

doc = Document()
style = Style("#demo")
route = Route()

# Adding title to document
doc.title("Testing")

# Creating parent div
parent = Parent("div")

# Adding home and about links
home_ = HTMLElement("a", href="/")
home_.text = "Home"

about = HTMLElement("a", href="/about")
about.text = "About"

parent.add_child(home_, about)

# Adding about content
about_content = HTMLElement("h1")
about_content.text = "About"

# Rendering routes
route.render("/", parent)
route.render("/about", about_content)

# Writing JavaScript code to file
with open('./output/script.js', 'w') as file:
    file.write(route.run())

# Adding style and body to document
doc.add_style(style)
doc.body(parent)

# Building the document
doc.build()
