import functools
import json
import re
import sys
from xml.sax import parseString, parse
from xml.sax.handler import ContentHandler

class TemplixHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.element_stack = []

    @property
    def current_element(self):
        return self.element_stack[-1]

    def startElement(self, name, attrs):
        self.element_stack.append({
            "name": name,
            "attributes": dict(attrs),
            "children": [],
            "value": ""
        })

    def endElement(self, name):
        clean(self.current_element)
        if len(self.element_stack) > 1:
            child = self.element_stack.pop()
            self.current_element["children"].append(child)

    def characters(self, content):
        self.current_element["value"] += content

def clean(element):
    element["value"] = element["value"].strip()
    for key in ("attributes", "children", "value"):
        if not element[key]:
            del element[key]

def converter(node, indent=0):
    tab = " " * indent
    name = node["name"]
    attrs = node.get("attributes", {})
    children = node.get("children", [])
    value = node.get("value", None)

    out = f"{tab}CreateElement(\n"
    out += f"{tab}    \"{name}\",\n"
    out += f"{tab}    {json.dumps(attrs)},\n"

    # Case 1: only a text node
    if value and not children:
        out += f"{tab}    \"\"\" {value} \"\"\"\n"
        out += f"{tab})"
        return out

    # Case 2: no children and no value
    if not children and not value:
        out += f"{tab}    \"\"\n"
        out += f"{tab})"
        return out

    # Case 3: text + children
    if value:
        out += f"{tab}    \"\"\" {value} \"\"\",\n"

    # Case 4: children
    for child in children:
        out += converter(child, indent + 4) + ",\n"
        out += f"{tab}    \"\"\"\"\"\",\n"

    out += f"{tab})"
    return out

def extract_xml(code: str) -> str:
    # Extract EXACTLY the content inside return(...)
    match = re.search(r"return\s*\(\s*(<.*>)\s*\)", code, re.S)
    if not match:
        raise ValueError("No valid XML found inside return(...)")
    return match.group(1).strip()


def parse_xml(html: str):
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    handler = TemplixHandler()
    parseString(html, handler)
    root = handler.current_element
    return root


def transform_function(code: str) -> str:
    html = extract_xml(code)
    tree = parse_xml(html)
    rendered = converter(tree)

    # Replace the return(...) block with CreateElement(...) result
    return re.sub(
        r"return\s*\([^)]*\)",
        f"return (\n{rendered}\n)",
        code,
        flags=re.S
    )


templixHandler = TemplixHandler()

# file_data = open(f"{fileN}.html", "r")

#
# final_output = transform_function(file_data.read())
# final_output = re.sub("@view", "", final_output)
# print("\n=== TRANSFORMED PYTHON ===\n")
# print(final_output)

# with open(f"{fileN}.json", "w") as f:
#   f.write(json.dumps(final_output, indent=4))
#
# with open(f"{fileN}.py", "w") as f:
#     f.write(final_output)

def translate_file(templix: str, py_path: str) -> None:
    with open(templix, 'r', encoding='utf-8') as fh:
        pkd_contents = fh.read()

    try:
        py_contents = transform_function(pkd_contents)
        py_contents = py_contents.replace("@view\n", "\n")
    except SyntaxError:
        sys.stderr.write('Failed to convert: %s\n' % templix)
        return

    with open(py_path, 'w', encoding='utf-8') as fh:
        fh.write(py_contents)