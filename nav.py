# c => c + 1

import inspect

my_function = lambda c: c + 1

source_code = inspect.getsource(my_function)
# print(type(source_code))

source_code = source_code.replace('lambda', '').replace(':', " =>")

print(source_code)

import inspect


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

def lambda_to_js(fn):
    # get source code of the lambda
    source = inspect.getsource(fn).strip()

    # Example: "lambda c: c + 1"
    # Remove assignment like  "x = lambda c: c + 1"
    if "=" in source:
        source = source.split("=",1)[1].strip()

    # Remove spaces
    source = source.replace("\n", "").strip()

    # Now convert Python lambda → JS arrow
    # lambda c: c + 1  →  c => c + 1
    if source.startswith("lambda"):
        args_body = source[len("lambda"):].strip()
        args, body = args_body.split(":", 1)
        args = args.strip()
        body = body.strip()
        return f"{args} => {body}"

    raise ValueError("Not a lambda")


class State:
    def __init__(self, name, initial):
        self.name = name
        self.initial = initial

    def set(self, fn):
        if callable(fn):
            source = inspect.getsource(fn).strip()

            # handle "count.set(lambda c: c + 1)"
            source = source.split("=", 1)[-1].strip()

            source = source.replace("lambda", "").replace(":", " =>")
            source = source.removeprefix("count.set(").removesuffix(")")

            return f"{self.name}.set({source})"

        return f"{self.name}.set({fn})"

    def get(self):
        return f"{self.name}.get()"



_state_counter = 0

@__js__
def Create(initial):
    global _state_counter
    var = f"state{_state_counter}"
    _state_counter += 1
    return State(var, initial)

def Component(func):
    name = func.__name__[0].upper() + func.__name__[1:]

    def wrapper():
        root = func()

        lines = []
        lines.append(f"function {name}() {{")

        # find all global states used
        for i in range(_state_counter):
            lines.append(f"  const state{i} = Create(0);")

        # return h(...)
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


count = Create(0)

print(
count.set(lambda c: c + 1))