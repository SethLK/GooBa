
from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, CodeBlock, Function, view
from GooBa.component.DataClass import CreateData
from another import Sompage
from testing import another_2, another

# from something import main_page, main_page2

doc = Document()
router = Router()
dataType = CreateData("name", "email")
# print(dataType[0])

# def another_2():
#     return (
# CreateElement(
#     "div",
#     {  },
#     CreateElement(
#         "label",
#         { "htmlFor": "inputField" },
#         "Enter text:"
#     ),
#     CreateElement(
#         "input",
#         { "id": "inputField", "type": "text", "value": "inputValue", "onChange": "handleInputChange" },
#         ""
#     ),
#     CreateElement(
#         "p",
#         {  },
#         "You typed: {inputValue}"
#     )
# )
# )

@Component
@view
def homePage():
    count = Create(1)
    return (CreateElement("div", {},
                          CreateElement("h1", {}, "Home Page"),
                          CreateElement("p", {}, f"{count.get()}"),
                            CreateElement("button", { "on:click": f"{count.set(lambda c: c *2)}"}, "+1")
  ))



# print(homePage())

# Clean, readable syntax
home = CreateElement("div", {},
                     CreateElement("h1", {}, "Home Page"),
    CreateElement("a", { "href": "/product" }, "Go to Product")
  )

home.style = {
    "background-color": "#00f",
    "color": "#fff",
}

about = CreateElement('div', {'id': 'about'},
    CreateElement('h1', {}, 'About'),
)

# fetching some data

fetch = Fetch("https://jsonplaceholder.org/posts/1")
post_1 = fetch.get()

person_page = CreateElement(
    'div',
    {
        'id': 'person-page',
    },

    'hello',
    # post_1.title
)

router.render('/', homePage())
router.render('/about', about)
router.render('/person', person_page)
router.render('/something', Sompage())
router.render('/:id', CreateElement('div', {'id': 'param'}, 'User ID: ${ctx.params.id}'))
router.render('/:title/:content', another())
router.render('/something/:id', CreateElement('div', {'id': 'param'}, 'User ID: ${ctx.params.id}'))

router.run('root')
doc.build()
