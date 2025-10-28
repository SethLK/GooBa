
from GooBa import Document, CreateElement, Router
from something import main_page, main_page2

doc = Document()
router = Router()

# Clean, readable syntax
home = CreateElement('div', {'id': 'home'},"Hello",
    CreateElement('h1', {}, 'Welcome to GooBa!', ),
    CreateElement('p', {}, 'This works perfectly!'),
    CreateElement('button', {'onclick': "alert('Hello!')"}, 'Click me'),
)

home.style = {
    "background-color": "#00f",
    "color": "#fff",
}

# about = CreateElement('h1', {'id': 'about'}, 'About',
#                       main_page(),
#                       tag()
#                       )

about = CreateElement('div', {'id': 'about'},
    CreateElement('h1', {}, 'About'),
    main_page(),
    main_page2(),
    main_page2()
)


router.render('/', home)
router.render('/about', about)
router.render('/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

router.render('/something/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

router.run('root')
doc.build()