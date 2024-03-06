from component.HTMLElement import HTMLElement
from component.Image import Image
from component.parent import Parent

def fileHandle(file_path, elements):
    with open(file_path, 'r') as file:
        file_content = file.read()

    modified_content = '\n'.join([str(element) for element in elements])

    # Write modified content back to file
    with open('./output/index.html', 'a') as file:
        file.write(modified_content)
        print(modified_content)


# Example usage:
h1 = HTMLElement("h1", id="demo", class_name="demo")
h1.set_text("Hello")

h2 = HTMLElement("h2", id="subtitle", class_name="subtitle")
h2.set_text("Welcome to my website")

paragraph = HTMLElement("p", id="content", class_name="content")
paragraph.set_text("This is the content of my webpage")

div_1 = Parent("div")
div_1.add_child(paragraph)



fileHandle('./output/index.html', [h1, h2, div_1])
