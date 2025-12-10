

import re
import sys
import json
from xml.sax import parseString
from xml.sax.handler import ContentHandler


_JSX_PREFIX = "__TEMPLIX_EXPR__"
_JSX_SUFFIX = "__END__"


def preprocess_jsx_attributes(html: str) -> str:
    pattern = re.compile(r'([:\w-]+)\s*=\s*{(.*?)}', flags=re.S)

    def repl(m):
        attr = m.group(1)
        expr = m.group(2).strip()
        # escape double-quotes (so XML attribute stays valid)
        expr_esc = expr.replace('"', "&quot;")
        return f'{attr}="{_JSX_PREFIX}{expr_esc}{_JSX_SUFFIX}"'

    return pattern.sub(repl, html)


def remove_html_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


class TemplixHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.element_stack = []

    @property
    def current_element(self):
        return self.element_stack[-1]

    def startElement(self, name, attrs):
        # attrs is an AttributesImpl; convert to dict
        self.element_stack.append({
            "name": name,
            "attributes": dict(attrs),
            "children": [],
            "value": ""
        })

    def endElement(self, name):
        # finalize current element and push as child to parent (if any)
        clean(self.current_element)
        if len(self.element_stack) > 1:
            child = self.element_stack.pop()
            self.current_element["children"].append(child)

    def characters(self, content):
        # accumulate text nodes
        if self.element_stack:
            self.current_element["value"] += content


def clean(element):
    """Trim value and remove empty keys to keep dicts small."""
    if "value" in element:
        element["value"] = element["value"].strip()
    for key in ("attributes", "children", "value"):
        if key in element and (element[key] == {} or element[key] == [] or element[key] == ""):
            element.pop(key, None)


def parse_html_to_tree(html: str):

    wrapped = f"<root>{html}</root>"
    handler = TemplixHandler()
    parseString(wrapped, handler)
    root = handler.current_element  # this is the <root> element

    children = root.get("children", [])
    if len(children) == 1:
        return children[0]
    # create a synthetic wrapper node so converter always gets a single node
    return {"name": "div", "attributes": {}, "children": children}



def convert_attributes(attrs: dict) -> dict:

    out = {}
    for k, v in attrs.items():
        if isinstance(v, str) and v.startswith(_JSX_PREFIX) and v.endswith(_JSX_SUFFIX):
            js = v[len(_JSX_PREFIX):-len(_JSX_SUFFIX)]
            js = js.replace("&quot;", '"')
            out[k] = {"__raw_js__": js}
        else:
            out[k] = v
    return out


def render_attrs_python_literal(attrs: dict) -> str:

    parts = []
    for k, v in attrs.items():
        key_repr = json.dumps(k)  # safe quoting of key
        if isinstance(v, dict) and "__raw_js__" in v:
            js_code = v["__raw_js__"]
            # Use json.dumps to properly escape newlines etc inside the JS string
            parts.append(f"{key_repr}: {{'__raw_js__': {json.dumps(js_code)}}}")
        else:
            parts.append(f"{key_repr}: {json.dumps(v)}")
    return "{ " + ", ".join(parts) + " }"


def converter(node: dict, indent: int = 0) -> str:

    tab = " " * indent
    name = node["name"]
    attrs = convert_attributes(node.get("attributes", {}))
    children = node.get("children", [])
    value = node.get("value", None)

    out = f"{tab}CreateElement(\n"
    out += f'{tab}    {json.dumps(name)},\n'
    out += f'{tab}    {render_attrs_python_literal(attrs)},\n'

    # Case: text only
    if value and not children:
        text_repr = value
        out += f'{tab}    {json.dumps(text_repr)}\n'
        out += f"{tab})"
        return out

    # Case: no children, no value
    if not children and not value:
        out += f'{tab}    ""\n'
        out += f"{tab})"
        return out

    # Case: text + children
    if value:
        out += f'{tab}    {json.dumps(value)},\n'

    # Children
    for i, child in enumerate(children):
        out += converter(child, indent + 4)
        if i != len(children) - 1:
            out += ",\n"
        else:
            out += "\n"
    out += f"{tab})"
    return out


def extract_return_block(code: str):
    m = re.search(r"\breturn\s*\(", code)
    if not m:
        return None
    start_paren = m.end() - 1  # position of '('
    i = start_paren + 1
    depth = 1
    while i < len(code) and depth > 0:
        c = code[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        i += 1
    if depth != 0:
        raise ValueError("Unbalanced parentheses in return(...) block")
    # block_text excludes the outer parentheses
    block_text = code[start_paren + 1: i - 1]
    return (m.start(), start_paren, i, block_text)

def _gather_view_replacements(source_code: str):
    replacements = []
    view_pattern = re.compile(r"@view\s+def\s+(\w+)\s*\(\s*\)\s*:", flags=re.M)
    for vm in view_pattern.finditer(source_code):
        search_start = vm.end()
        tail = source_code[search_start:]
        info = extract_return_block(tail)
        if not info:
            continue
        abs_paren_start = search_start + info[1]
        abs_paren_end = search_start + info[2]
        block_text = info[3]

        # preprocess -> parse -> convert
        html = remove_html_comments(block_text)
        html = preprocess_jsx_attributes(html)
        tree = parse_html_to_tree(html)
        rendered = converter(tree)
        # replacement = f"return (\n{rendered}\n)"
        replacement = f"(\n{rendered}\n)"
        replacements.append((abs_paren_start, abs_paren_end, replacement))
    return replacements


def transform_function(source_code: str) -> str:
    """
    Full transform: collects replacements and then applies them from end -> start to avoid index shifting.
    """
    replacements = _gather_view_replacements(source_code)
    if not replacements:
        return source_code

    # Apply replacements from end to start so indices remain valid
    new_code = source_code
    for start_idx, end_idx, replacement in sorted(replacements, key=lambda x: x[0], reverse=True):
        new_code = new_code[:start_idx] + replacement + new_code[end_idx:]
    return new_code


# ---------------------------
# File-level translator helper
# ---------------------------

def translate_file(templix_path: str, py_path: str) -> None:
    with open(templix_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    try:
        out = transform_function(src)
    except Exception as e:
        sys.stderr.write(f"Failed to transform {templix_path}: {e}\n")
        raise
    with open(py_path, "w", encoding="utf-8") as fh:
        fh.write(out)


# ---------------------------
# CLI
# ---------------------------
#
# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Usage: python Templix.py <source.templix> <out.py>")
#         sys.exit(1)
#     src = sys.argv[1]
#     dst = sys.argv[2]
#     translate_file(src, dst)
#     print(f"Transformed {src} -> {dst}")
