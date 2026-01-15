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
