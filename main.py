from component.parent import Parent
from router.router import Router
from component.HTMLElement import HTMLElement, Link
from component.Document import Document
from component.style import Style, Css

doc = Document()
root = Parent("div", id="root")

head_ = Css("""
    h1{
    color: blue;
    }
""", "style_")
head_.render()

navBar = Parent("nav")

homeLink = Link("/")
homeLink.text = "Home"

AboutLink = Link("/about")
AboutLink.text = "About"

ContactLink = Link("/contact")
ContactLink.text = "Contact"

navBar.add_child(homeLink, AboutLink, ContactLink)

homePage = Parent("div")
HomeText = HTMLElement("h1")
HomeText.text = "Home"
homePage.add_child(HomeText)

aboutPage = Parent("div")
aboutText = HTMLElement("h1")
aboutText.text = "About"
aboutPage.add_child(aboutText)

contactPage = Parent("div")
contactText = HTMLElement("h1")
contactText.text = "Contact"
contactPage.add_child(contactText)

router = Router()

router.render("/", homePage)
router.render("/about", aboutPage)
router.render("/contact", contactPage)

router.run()

doc.body(navBar, root)
doc.add_Head(head_.apply())

doc.build()
