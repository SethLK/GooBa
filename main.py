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

root = Parent("div", id="root")

# Creating parent div
parent = Parent("div")

# Adding home and about links
home_ = HTMLElement("a", href="/")
home_.text = "Home"

about = HTMLElement("a", href="/about")
about.text = "About"

contact = HTMLElement("a", href="/contact")
contact.text = "Contact"

navBar = Parent("nav")
navBar.add_child(home_, about, contact)

parent.add_child(navBar)

homePage = HTMLElement("h1")
homePage.text = "Home Page"

aboutPage = HTMLElement("h1")
aboutPage.text = "About page"

contactPage = HTMLElement("h1")
contactPage.text = "Contact Page"


route.render("/", homePage)
route.render("/about", aboutPage)
route.render("/contact", contactPage)


# Writing JavaScript code to file
with open('./output/script.js', 'w') as file:
    file.write(route.run())

# Adding style and body to document
doc.add_style(style)
doc.body(parent, root)

# Building the document
doc.build()
