from component.Document import Document
from component.parent import Parent
from component.style import Css

import asyncio
import aiohttp

doc = Document()
root = Parent("div")

style_file = Css("""h1{
color: red; 
}""")

# Add a root element with id 'root' where the h1 elements will be appended
root.attributes['id'] = 'root'

async def fetch_data():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jsonplaceholder.typicode.com/todos') as response:
                if not response.ok:
                    raise Exception('Network response was not ok')
                data = await response.json()
                for i in range(6):
                    h1 = f"<h1>{data[i]['title']}</h1>"
                    # Append the h1 elements to the root
                    root.add_child(h1)
    except Exception as error:
        print('Error:', error)

async def main():
    # Fetch data asynchronously
    await fetch_data()
    # Build the HTML document after fetching data
    doc.body(root)
    doc.add_Head(style_file.render())
    doc.build()

# Run the event loop
asyncio.run(main())
