
from GooBa import Document, CreateElement, Router, CreateStyle
# from something import main_page, main_page2
from something import user_page

doc = Document()
router = Router()



# Clean, readable syntax
home = CreateElement('div', {'id': 'home'},"Hello",
    CreateElement('h1', {}, 'Welcome to GooBa!', ),
    CreateElement('p', {}, 'This works perfectly!'),
    CreateElement('button', {'onclick': "alert('Hello!')"}, 'Click me'),
                     user_page(),
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
    # main_page(),
    # main_page2(),
    # main_page2()
)

router.render('/', home)
# router.render('/user', User_page())
router.render('/about', about)
router.render('/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

router.render('/something/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

# doc.appendHead(pageStyle)

router.run('root')
doc.build()