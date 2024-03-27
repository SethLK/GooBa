import requests
from component.parent import Parent
from component.Document import Document
from component.HTMLElement import HTMLElement
from component.style import Style
from router.route import Route
from component.form import Form, Label, InputField

doc = Document()
style = Style("#demo")
route = Route()

# Adding title to document
doc.title("Testing")

# Create the root and parent div
root = Parent("div", id="root")

UserNameLabel = Label("Username\n", "Username")
PasswordLabel = Label("Password\n", "password")


form = Form()

username = InputField("Username\n")
username.label = UserNameLabel

password = InputField("Password\n")
password.label = PasswordLabel
password.type = "password"

submit = InputField("Submit")
submit.type = "submit"


form.addFields(username, password, submit)

root.add_child(form)


doc.add_style(style)
doc.body(root)

# Build the document
doc.build()
