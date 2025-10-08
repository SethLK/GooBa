# from GooBa import Document, CreateElement, CreateStyle, CreateForm, Methods
#
# # Create a new document
# doc = Document()
#
# # Create elements
# div = CreateElement("div", id="main-div")
# div.style = {
#     "background-color": "blue"
# }
#
# form = CreateForm(action='/submit', method=Methods.POST.value, id='myForm')
# form.add_label(for_="username", text="Username")
# form.add_input(input_type='text', name='username', placeholder='Enter your username')
# form.add_label(for_="password", text="Password")
# form.add_input(input_type='password', name='password', placeholder='Enter your password')
# form.add_label(for_="email", text="Email")
# form.add_input(input_type='email', name='email', placeholder='Enter your email')
# form.add_label(for_="comments", text="Comment")
# form.add_textarea(name='comments', rows=5, cols=40, placeholder='Your comments here...')
# form.add_button(button_type='submit', text='Submit')
#
# HomePage = CreateStyle()
# HomePage.style(".h1", {
#     "color": "blue",
# })
#
# doc.appendHead(HomePage)
#
# div.appendChild(form)
#
# doc.body(div)
#
# doc.build()

#
# from GooBa import Document, CreateElement, Router
#
# # Initialize Document and Router
# doc = Document()
#
# container = CreateElement('div', id='root')
#
# router = Router()
#
# home = CreateElement('h1', { id : 'home' }, 'Home')
#
# about = CreateElement('h1', id='about')
# about.text = 'About'
#
# # For dynamic routes, use template placeholders like {{id}}
# param = CreateElement('div', id='param')
# param.text = 'User ID: {{id}}'  # This will be replaced with actual ID
#
# router.render('/', home)
# router.render('/about', about)
# router.render('/<int:id>', param)  # This will become '/:id' in Page.js
#
# router.run('root')
# doc.body(container)
#
# doc.build()

from GooBa import Document, CreateElement, Router

doc = Document()
container = CreateElement('div',{'id': 'root'})
router = Router()

# Clean, readable syntax
home = CreateElement('div', {'id': 'home'},
    CreateElement('h1', {}, 'Welcome to GooBa!'),
    CreateElement('p', {}, 'This works perfectly!'),
    CreateElement('button', {'onclick': "alert('Hello!')"}, 'Click me')
)

home.style = {
    "background-color": "#00f",
    "color": "#fff",
}

about = CreateElement('h1', {'id': 'about'}, 'About')

# param = CreateElement('div', {'id': 'param'}, 'User ID: {{id}}')

router.render('/', home)
router.render('/about', about)
router.render('/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))

router.render('/something/<id>', CreateElement('div', {'id': 'param'}, 'User ID: {{id}}'))
#
# router.render('/api/<id>/<action>',
#     CreateElement('div', {'class_name': 'api'},
#         'API /{{id}}/{{action}}'
#     )
# )

router.run('root')
doc.body(container)
doc.build()