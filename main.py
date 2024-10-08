from GooBa import Document, CreateElement, CreateStyle, CreateForm, Methods

# Create a new document
doc = Document()

# Create elements
div = CreateElement("div", id="main-div")
div.style = {
    "background-color": "blue"
}

form = CreateForm(action='/submit', method=Methods.POST.value, id='myForm')
form.add_label(for_="username", text="Username")
form.add_input(input_type='text', name='username', placeholder='Enter your username')
form.add_label(for_="password", text="Password")
form.add_input(input_type='password', name='password', placeholder='Enter your password')
form.add_label(for_="email", text="Email")
form.add_input(input_type='email', name='email', placeholder='Enter your email')
form.add_label(for_="comments", text="COmment")
form.add_textarea(name='comments', rows=5, cols=40, placeholder='Your comments here...')
form.add_button(button_type='submit', text='Submit')

HomePage = CreateStyle()
HomePage.style(".h1", {
    "color": "blue",
})

doc.appendHead(HomePage)

div.appendChild(form)

doc.body(div)

doc.build()
