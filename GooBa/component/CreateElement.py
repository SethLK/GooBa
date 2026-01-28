import inspect
import re

from GooBa.Extern import JSExpr, EventHandler, EventTargetValue


class Node:
    """Base class for all AST nodes"""
    pass


class JSNode(Node):
    """Anything that outputs RAW JS"""
    def to_h(self):
        raise NotImplementedError

class G(JSNode):
    def __init__(self, *branches):
        self.branches = branches
        self.type = "element"

    def to_h(self):
        lines = [b.to_js() for b in self.branches]
        body = "\n".join(lines)

        print(body)

        return f"(function() {{\n{body}\n}})()".strip()

    def __str__(self):
        # just delegate to to_h
        return self.to_h()



class CreateElement:

    _id_counter = 0


    def __init__(self, tag, attributes=None, *children):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = list(children)
        self.style = {}
        self._id = CreateElement._id_counter
        self.type = "element"
        CreateElement._id_counter += 1

    def appendChild(self, *children):
        self.children.extend(children)
        return self

    def setAttribute(self, key, value):
        self.attributes[key] = value
        return self

    def to_h(self, depth=0):
        indent = "    " * depth

        if isinstance(self, str) or self.tag == "#text":
            text = self.children[0] if isinstance(self, CreateElement) else self
            return indent + f"\"{text}\""

        attrs_items = []
        for key, value in self.attributes.items():
            # print(key, value, type(value))

            if key.startswith("on:"):
                event_name = key.split(":", 1)[1]
                # print(value)
                if event_name == "input":
                    #
                    print(value)
                    source = ""
                    if "e.target.value" in value:
                        source = f"on: {{ {event_name}: (e) => {value}}}"
                    # attrs_items.append(value)
                    # value_str = inspect.getsource(value).strip()
                    # print(value_str)
                    #
                    # source = value_str.replace(":", "").split(" ")[2:]
                    # code = "" + source[1]
                    #
                    # print(code)
                    # param = code.replace("newItem.set(", "").replace(")", "")
                    # print(param)
                    # print(source)
                    # source = f"on: {{ {event_name}: ({source[0]}) => {value()}}}"
                    # print(source)
                    attrs_items.append(source)

                    continue

                if "e.preventDefault();" in value:
                    # print(f"{type(value)} -> {value}")
                    # for v in value:
                    #     print("->" + v)

                    d_value = "{ \n"
                    for v in value:
                        d_value += v + "\n"
                    d_value += "\n}"
                    # print("d -> " + d_value)

                    attrs_items.append(f'on: {{ {event_name}: (e) => {d_value} }}')
                    # print(f'on: {{ {event_name}: (e) => {value} }}'.strip())
                    continue
                else:
                    attrs_items.append(f'on: {{ {event_name}: () => {value} }}')
                    continue

            if value.endswith("()"):
                attrs_items.append(f'value: {value}')
                continue

            else:
                attrs_items.append(f"{key}: \"{value}\"")
                continue

        attr_js = "{ " + ", ".join(attrs_items) + " }" if attrs_items else "{}"

        lines = []
        for child in self.children:
            if hasattr(child, "to_h"):
                lines.append(("    " * (depth + 1)) + child.to_h())
            else:
                lines.append(("    " * (depth + 1)) + f"`{child}`")


        # children_block = "[\n" + ",\n".join(lines) + "\n" + indent + "]"
        children_block = f"[\n{',\n'.join(lines)}\n{indent}]" if lines else ""

        return f'{indent}h("{self.tag}", {attr_js}, {children_block})'


    @staticmethod
    def _escape_js(value):
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

    def __str__(self):
        return self.to_h()
