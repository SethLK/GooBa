
from GooBa import Document, CreateElement, Router, CreateStyle, Fetch

# from something import main_page, main_page2

doc = Document()
router = Router()



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
    # post_1.title
)

router.render('/', home)
router.render('/about', about)
router.render('/person', person_page)
router.render('/:id', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

router.render('/something/:id', CreateElement('div', {'id': 'param'}, 'User ID: ${ctx.params.id}'))

router.run('root')
doc.build()

print(home)
print(home.to_h())




something = "/:id/:name"
something = something.split("/:")
print(something)