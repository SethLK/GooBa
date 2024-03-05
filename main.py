from component.component import HTMLElement, Image

h1 = HTMLElement("h1", id="demo", class_name="demo")
h1.set_text("Hello")

def fileHundle(_file_path, _content):
    with open(_file_path, 'r') as file:
        return file.read()

    modified_content = f'{file_content} \n {h1}'

    # Write modified content back to file
    with open('./output/index.html', 'w') as file:
        file.write(modified_content)