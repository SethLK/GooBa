import inspect
import re

from GooBa.Condition.Condition import Expr
# from ..Condition.Condition import Expr

class CodeBlock:
    def __init__(self, code: str, filename: str = None):
        self.code = code
        self.filename = filename

    def save_to_file(self):
        if self.filename:
            try:
                with open(f'./output/{self.filename}.js', 'w') as file:
                    file.write(self.code)
            except IOError as e:
                print(f"Error writing to file: {e}")
                return None
            return self.filename
        return None

    def get_code_tag(self, type):
        if self.code:
            if type:
                return f'<script type="{type}">{self.code}</script>'
            else:
                return f'<script>{self.code}</script>'
        return None

    def __str__(self):
        return self.code


def __js__(func):
    return func


class ComponentContext:
    def __init__(self):
        self.states = []
        self.requests = []
        self.state_id = 0
        self.request_id = 0


_current_context = ComponentContext()

_state_counter = 0
_state_registry = []
_request_counter = 0
_request_registry = []

class Create:
    def __init__(self, initial):
        global _current_context

        ctx = _current_context
        self.id = ctx.state_id
        ctx.state_id += 1

        self.initial = initial
        self.name = f"state{self.id}"

        ctx.states.append(self)

    def __str__(self):
        return f"const state{_state_counter} = Create({self.initial});"

    def value(self):
        return Expr(f"{self.name}.get()")

    def text(self):
        return f"${{{self.name}.get()}}"

    def get(self):
        return f"${{{self.name}.get()}}"

    def set(self, fn):
        if callable(fn):
            source = inspect.getsource(fn).strip()
            # print(source)
            start = source.find("lambda")
            end = source.find(")}", start)

            source = source[start:end]
            source = source.replace("lambda", "").replace(":", " =>")

            return f"{self.name}.set({source})"

        if type(fn) == str:
            return f"{self.name}.set(`{fn}`)"

        return f"{self.name}.set({fn})"


class useRequest:

    def __init__(
        self,
        url="",
        method="GET",
        headers=None,
        body=None,
        mode=None,
        credentials=None,
        cache=None,
        redirect=None,
        referrer=None,
        referrerPolicy=None,
        signal=None
    ):
        global _current_context

        ctx = _current_context
        self.id = ctx.request_id
        ctx.request_id += 1

        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.mode = mode
        self.credentials = credentials
        self.cache = cache
        self.redirect = redirect
        self.referrer = referrer
        self.referrerPolicy = referrerPolicy
        self.signal = signal

        ctx.requests.append(self)

    def _build_options(self):
        options = {
            "method": self.method
        }

        if self.headers:
            options["headers"] = self.headers

        if self.body and self.method not in ("GET", "HEAD"):
            options["body"] = f"JSON.stringify({self.body})"

        if self.mode:
            options["mode"] = self.mode

        if self.credentials:
            options["credentials"] = self.credentials

        if self.cache:
            options["cache"] = self.cache

        if self.redirect:
            options["redirect"] = self.redirect

        if self.referrer:
            options["referrer"] = self.referrer

        if self.referrerPolicy:
            options["referrerPolicy"] = self.referrerPolicy

        return options

    def _options_js(self):
        opts = self._build_options()
        lines = []

        for key, value in opts.items():
            if isinstance(value, str) and not value.startswith("JSON.stringify"):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")

        return ",\n    ".join(lines)


    def emit(self):
        return f"""
  const fetch{self.id} = useRequest();
  useOnce(() => {{
    fetch{self.id}.request("{self.url}", {{
        {self._options_js()}
    }});
  }});
  
""".rstrip()

    def to_js(self):
        return self.emit()

    def __str__(self):
        return self.emit()

    def get(self, key):
        return f"${{fetch{self.id}.data.get()?.{key}}}"

    def value(self):
        return f"fetch{self.id}.data.get()"

def Component(func):
    name = func.__name__[0].upper() + func.__name__[1:]

    def wrapper():
        global _current_context
        _current_context = ComponentContext()

        root = func()
        string_py = inspect.getsource(func).strip()

        ctx = _current_context
        _current_context = None

        lines = [f"function {name}() {{"]

        for req in ctx.requests:
            lines.append(req.emit())

        # 2️⃣ state
        for state in ctx.states:
            lines.append(
                f"  const {state.name} = Create({state.initial});"
            )

        # 3️⃣ render
        lines.append("  return " + root.to_h(depth=2) + ";")
        lines.append("}")

        return "\n".join(lines)

    return wrapper


class JSFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def emit(self):
        args = ", ".join(map(str, self.args))
        return f"{self.name}({args})"


class JSFunction:
    def __init__(self, name, py_fn):
        self.name = name
        self.py_fn = py_fn   # stored, NOT executed
        self.body = None     # AST

    def build(self):
        # execute Python function ONLY to collect AST
        self.body = self.py_fn()

    def emit(self):
        return f"""
function {self.name}() {{
  return {self.body};
}}
""".strip()

    def __call__(self, *args):
        # THIS IS THE KEY PART
        return JSFunctionCall(self.name, args)

def Function(py_fn):
    js_fn = JSFunction(py_fn.__name__, py_fn)
    js_fn.build()
    return js_fn




''''
# -----------------
    # JS DOM Generator
    # -----------------
    def to_js_dom(self, var_prefix="el", depth=0):
        indent = "    " * depth
        var_name = f"{var_prefix}_{self._id}_{self.tag.replace('#', '')}"

        lines = []
        if self.tag == "#text":
            content = self._escape_js(self.children[0]) if self.children else ""
            lines.append(f"{indent}const {var_name} = document.createTextNode(`{content}`);")
            return lines, var_name

        lines.append(f"{indent}const {var_name} = document.createElement('{self.tag}');")

        # Attributes
        for key, value in self.attributes.items():
            if key == "className":
                lines.append(f"{indent}{var_name}.className = '{self._escape_js(value)}';")
            elif key == "id":
                lines.append(f"{indent}{var_name}.id = '{self._escape_js(value)}';")
            # elif key.startswith("on"):
            #     lines.append(f"{indent}{var_name}.{key} = {value};")
            elif key.startswith("on"):
                # Wrap in a function if it's a JS expression string
                if isinstance(value, str) and not value.strip().startswith("function"):
                    lines.append(f"{indent}{var_name}.{key} = () => {value};")
                else:
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
'''


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


#     req_match = re.search(
#         r"(\w+)\s*=\s*useRequest\((.*?)\)\n",
#         string_py, re.S
#     )
#     if req_match:
#         req_body = req_match.group(2)
#         var = req_match.group(1)
#
#         url = re.search(r'url\s*=\s*"([^"]+)"', req_body)
#         method = re.search(r'method\s*=\s*"([^"]+)"', req_body)
#         headers = re.search(r'headers\s*=\s*(\{.*?\})', req_body, re.S)
#
#         url = url.group(1) if url else ""
#         method = method.group(1) if method else "GET"
#         headers = headers.group(1) if headers else "{}"
#
#         the_request = f"""
# const fetch{var} = useRequest();
# fetch{var}.request("{url}",{{
#     method: "{method}",
#     headers: {headers}
# }});
# """.strip()
#         print(the_request)
#     # print(url)
#     # print(req_match.group(2))
#
#
#         lines.append(the_request)



# def Component(func):
#     print(inspect.getsource(func).strip())
#     name = func.__name__[0].upper() + func.__name__[1:]
#
#     def wrapper():
#         global _state_registry, _request_registry
#
#         # 🔥 reset per component render
#         _state_registry = []
#         _request_registry = []
#         Create._id = 0
#         useRequest._id = 0
#
#         root = func()
#         lines = [f"function {name}() {{"]
#         #
#         # print(_request_registry)
#         #
#         # print(_state_registry)
#         print(_request_registry)
#
#         for req in _request_registry:
#             lines.append(req.emit())
#
#         # lines.append(
#         #     f"{globals()['useRequest']()}"
#         # )
#         for state in _state_registry:
#             lines.append(
#                 f"  const state{state.id} = Create({state.initial});"
#             )
#         # return h(...)
#         lines.append("  return " + root.to_h(depth=2) + ";")
#         lines.append("}")
#         return "\n".join(lines)
#     return wrapper


"""
export function Create<T>(initial: T): { 
    get: () => T;
    set: (value: T | ((prev: T) => T)) => void;
} {
    if (!current) {
        throw new Error("Create() must be called inside a hooked component");
    }

    const hooks = current.hooks;
    const idx = current.hookIndex++;

    if (hooks[idx] === undefined) {
        hooks[idx] = initial;
    }

    const get = () => hooks[idx] as T;

    const set = (value: T | ((prev: T) => T)) => {
        if (typeof value === "function") {
            hooks[idx] = (value as (prev: T) => T)(hooks[idx]);
        } else {
            hooks[idx] = value;
        }

        triggerRender();
    };


    return { get, set };
}

"""

# class State:
#     def __init__(self, name, initial):
#         self.name = name
#         self.initial = initial
#
#     def set(self, fn):
#         if callable(fn):
#             source = inspect.getsource(fn).strip()
#             print(source)
#             start = source.find("lambda")
#             end = source.find(")}", start)
#
#             source = source[start:end]
#             # print(source)
#             # # handle "count.set(lambda c: c + 1)"
#             # source = source.split("=", 1)[-1].strip()
#             # print(source)
#             source = source.replace("lambda", "").replace(":", " =>")
#             # print(source)
#             # source = source.removeprefix("count.set(").removesuffix(")")
#             # print(source)
#
#             return f"{self.name}.set({source})"
#
#         return f"{self.name}.set({fn})"
#
#     def get(self):
#         return f"${{{self.name}.get()}}"
#
# def Create(initial):
#     global _state_counter
#     var = f"state{_state_counter}"
#     _state_counter += 1
#     return State(var, initial)