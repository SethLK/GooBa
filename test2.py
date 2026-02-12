import code
import re
from xml.sax import parseString

from GooBa.Templix.myown import TemplixHandler, converter, _JSX_PREFIX, _JSX_SUFFIX

def extract_return_block(code: str):
    # x = re.search("[a-zA-Z]", code)
    #
    # print("The first white-space character is located in position:", x.start())
    # tree = ast.parse(code)
    #
    # for node in tree.body:
    #     if isinstance(node, ast.FunctionDef):
    #         for stmt in node.body:
    #             if not isinstance(stmt, ast.Return):
    #                 print(ast.unparse(stmt))
    # print(extract_function_body(code))

    m = re.search(r"\breturn\s*\(", code)
    # print("Code ->" + code)
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

def remove_html_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)



def preprocess_jsx_attributes(html: str) -> str:
    pattern = re.compile(r'([:\w-]+)\s*=\s*{(.*?)}', flags=re.S)

    def repl(m):
        attr = m.group(1)
        expr = m.group(2).strip()
        # escape double-quotes (so XML attribute stays valid)
        expr_esc = expr.replace('"', "&quot;")
        return f'{attr}="{_JSX_PREFIX}{expr_esc}{_JSX_SUFFIX}"'

    return pattern.sub(repl, html)

def fix_tag_spaces(html: str) -> str:
    # Replace "< p >" with "<p>"
    html = re.sub(r"<\s*([A-Za-z0-9:_-]+)\s*>", r"<\1>", html)
    html = re.sub(r"<\s*/\s*([A-Za-z0-9:_-]+)\s*>", r"</\1>", html)
    return html

def fix_html_void_tags(html: str) -> str:
    voids = ["area", "base", "br", "col", "embed", "hr", "img",
             "input", "link", "meta", "param", "source", "track", "wbr"]

    for tag in voids:
        # convert <hr> to <hr />
        html = re.sub(fr"<{tag}\s*>", fr"<{tag} />", html)
    return html



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




def _gather_view_replacements(source_code: str):
    replacements = []
    view_pattern = re.compile(r"\s*:", flags=re.M)
    for vm in view_pattern.finditer(source_code):
        search_start = vm.end()
        tail = source_code[search_start:]
        info = extract_return_block(tail)
        if not info:
            continue
        abs_paren_start = search_start + info[1]
        abs_paren_end = search_start + info[2]
        block_text = info[3]
        print("INfo" + block_text)

        # preprocess -> parse -> convert
        html = remove_html_comments(block_text)
        html = preprocess_jsx_attributes(html)
        html = fix_tag_spaces(html)
        html = fix_html_void_tags(html)
        tree = parse_html_to_tree(html)
        # print("Tree ->" + tree)
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
    # print(replacements)
    if not replacements:
        return source_code

    # Apply replacements from end to start so indices remain valid
    new_code = source_code
    for start_idx, end_idx, replacement in sorted(replacements, key=lambda x: x[0], reverse=True):
        new_code = new_code[:start_idx] + replacement + new_code[end_idx:]
    return new_code


txt = """
def somefuntion():
    something = 1
    hi = "Helloo"
    print(hi)
    return (
        <div>
        <h2> HTML Forms hi</h2>
        <form action="/">
        <label for ="title"> First name: </label> <br>
        <input type="text" id="title" name="title" value={title.value()} on:input= {title.set(event.target.value)}/> <br/>
        <label for ="content"> Last name: </label> <br>
        <input type="text" id="content" name="content" value={content.value()} on:input= {content.set(event.target.value)} /> <br/> <br/>
        <input type="submit" value="Submit" />
        </form>
        <p> If you click the "Submit" button, the form-data will be sent to a page called </p>
        </div>
    )
""".strip()


# transform_function(txt)

txt_list = txt.splitlines()
# print(txt_list)
num_to_remove = 1
def extract_statements_before_return(code: str):
    out = []
    lines = code.splitlines()

    for line in lines:
        s = line.strip()

        if s.startswith("def "):
            continue

        if s.startswith("return"):
            break

        if s:
            out.append(s)

    return "\n".join(out)

print(extract_statements_before_return(txt))


