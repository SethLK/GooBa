import re


class CreateElement:
    """Pure DOM-like element builder (Python version of document.createElement)."""

    _id_counter = 0  # global unique counter for all created elements

    def __init__(self, localName, attributes=None, *children):
        self.tag = localName
        self.attributes = attributes or {}
        self.children = list(children)
        self.style = {}
        self._id = CreateElement._id_counter
        CreateElement._id_counter += 1

    # -----------------
    # DOM-like methods
    # -----------------
    def appendChild(self, *children):
        self.children.extend(children)
        return self

    def setAttribute(self, key, value):
        self.attributes[key] = value
        return self

    # -----------------
    # JS DOM Generator
    # -----------------
    def to_js_dom(self, var_prefix="el", depth=0):
        indent = "    " * depth
        var_name = f"{var_prefix}_{self._id}_{self.tag.replace('#', '')}"

        lines = []
        if self.tag == "#text":
            content = self._escape_js(self.children[0]) if self.children else ""
            lines.append(f"{indent}const {var_name} = document.createTextNode('{content}');")
            return lines, var_name

        lines.append(f"{indent}const {var_name} = document.createElement('{self.tag}');")

        # Attributes
        for key, value in self.attributes.items():
            if key == "className":
                lines.append(f"{indent}{var_name}.className = '{self._escape_js(value)}';")
            elif key == "id":
                lines.append(f"{indent}{var_name}.id = '{self._escape_js(value)}';")
            elif key.startswith("on"):
                lines.append(f"{indent}{var_name}.{key} = {value};")
            else:
                lines.append(f"{indent}{var_name}.setAttribute('{key}', '{self._escape_js(value)}');")

        # Styles
        for s_key, s_val in self.style.items():
            js_key = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), s_key)
            lines.append(f"{indent}{var_name}.style.{js_key} = '{self._escape_js(s_val)}';")

        # Children
        for child in self.children:
            # if callable(child):  # handle passed functions automatically
            #     child = child()

            if isinstance(child, str):
                text_node = CreateElement("#text", {}, child)
                child_lines, child_var = text_node.to_js_dom(var_prefix, depth + 1)
            elif isinstance(child, CreateElement):
                child_lines, child_var = child.to_js_dom(var_prefix, depth + 1)
            else:
                continue
            lines.extend(child_lines)
            lines.append(f"{indent}{var_name}.appendChild({child_var});")

        return lines, var_name

    @staticmethod
    def _escape_js(value):
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

    def render_js(self, root_id=None):
        lines, var_name = self.to_js_dom()
        if root_id:
            lines.append(f"document.getElementById('{root_id}').appendChild({var_name});")
        return "\n".join(lines)
