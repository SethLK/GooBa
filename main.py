from component.Document import Document
from component.parent import Parent
from component.style import Style, Css
from Extern.JavaScript import CodeBlock

doc = Document()
root = Parent("div")

js_code = """
async function fetchData() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/todos');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        for (let i = 0; i < 6; i++) {
            const h1 = document.createElement('h1');
            h1.textContent = data[i].title;
            document.getElementById('root').appendChild(h1);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    fetchData();
});
"""

style_file = Css("""h1{
color: red; 
}""")

# Add JavaScript code to the document's head
doc.add_Head("<script>" + js_code + "</script>")

# Add a root element with id 'root' where the h1 elements will be appended
root.attributes['id'] = 'root'

js_code = CodeBlock("alert('Hello World')", "alert")
js_code2 = CodeBlock("alert('Hello World 3')", "alert2")
# Build the HTML document
doc.body(root)
doc.add_Head(style_file.render())
doc.add_EternalJs(js_code.save_to_file())
doc.add_EternalJs(js_code2.save_to_file())
doc.build()
