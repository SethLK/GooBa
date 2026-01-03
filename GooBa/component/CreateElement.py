import re

# function h(tag, props = {}, children = []) {
#   return {
#     tag,
#     props,
#     children: mapTextNodes(withoutNulls(children)),
#     type: DOM_TYPES.ELEMENT
#   };
# }

# function mapTextNodes(children) {
#   return children.map(
#     (child) => typeof child === "string" ? hString(child) : child
#   );
# }

# export function AppHome() {
#   return h("div", {}, [
#     h("h1", {}, ["Home Page"]),
#     h("a", { href: "/product" }, ["Go to Product"])
#   ]);
# }

"""
import { createApp, h, Create } from "./dist/gooba.js";

// --- Components ---
export function AppHome() {
  return h("div", {}, [
    h("h1", {}, ["Home Page"]),
    h("a", { href: "/product" }, ["Go to Product"])
  ]);
}

export function NotFound() {
  return h("h2", {}, ["404 Page Not Found"]);
}


// --- Routing / Mounting ---
function render(component) {
  createApp({ view: () => component }).mount(document.getElementById("root"));
}

// Define all routes BEFORE page.start()
page("/", () => render(AppHome()));
page("/product", () => render(AppProduct()));
page("*", () => render(NotFound()));

page.start();
"""

class CreateElement:
    """Pure DOM-like element builder (Python version of document.createElement)."""

    _id_counter = 0  # global unique counter for all created elements

    def __init__(self, tag, attributes=None, *children):
        self.tag = tag
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

    def to_h(self, depth=0):
        indent = "    " * depth

        if isinstance(self, str) or self.tag == "#text":
            text = self.children[0] if isinstance(self, CreateElement) else self
            return indent + f"\"{text}\""

        attrs_items = []
        for key, value in self.attributes.items():
            if key.startswith("on:"):
                event_name = key.split(":", 1)[1]
                attrs_items.append(f'on: {{ {event_name}: () => {value} }}')
                continue

            else:
                attrs_items.append(f"{key}: \"{value}\"")

        attr_js = "{ " + ", ".join(attrs_items) + " }" if attrs_items else "{}"

        lines = []
        for child in self.children:
            if isinstance(child, CreateElement):
                lines.append(child.to_h(depth + 1))
            else:
                lines.append(("    " * (depth + 1)) + f"`{child}`")

        if lines:
            # children_block = "[\n" + ",\n".join(lines) + "\n" + indent + "]"
            children_block = f"[\n{',\n'.join(lines)}\n{indent}]"
        else:
            children_block = "[]"

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

    # def render_js(self, root_id=None):
    #     lines, var_name = self.to_js_dom()
    #     if root_id:
    #         lines.append(f"document.getElementById('{root_id}').appendChild({var_name});")
    #     return "\n".join(lines)
    # def render_js(self, root_id=None):
    #     lines, var_name = self.to_h()
    #     if root_id:
    #         lines.append(f"document.getElementById('{root_id}').appendChild({var_name});")
    #     return "\n".join(lines)