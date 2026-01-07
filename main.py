
from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest

doc = Document()
router = Router()

# def g(cond, then_, else_=None):
#     return then_ if cond else else_

# class g:
#     def __init__(self, cond, then_, else_=None):
#         self.cond = cond
#         self.then_ = then_
#         self.else_ = else_
#
#     def to_h(self):
#         return (
#             f"""
# (() => {{
#
#     }})(),
# """
#         )

# if (num.get() < 5) {
#         return h( "p" , {}, [ `Number is less than 5: ${num.get()}` ]);
#       }
#
# class G_if:
#     def __init__(self, cond, value):
#         self.cond = cond
#         self.value = value
#
#     def to_h(self):
#         if isinstance(self.value, CreateElement):
#             return (
#                 f"""
#                 if ({self.cond}) {{
#                     return {self.value.to_h()};
#                     }}
# """
#             )
#         return None
#
#
# class G_else:
#     def __init__(self, value):
#         self.value = value
#
#     def to_h(self):
#         if isinstance(self.value, CreateElement):
#             return self.value.to_h()
#         return None
#
#
# class G:
#     def __init__(self, *branches):
#         self.branches = branches
#
#     def to_h(self):
#         lines = []
#
#         for b in self.branches:
#             lines.append(b.to_h())
#
#         body = "\n".join(lines)
#         print(body)
#
#         return f"""(() => {{
# {body}
# return null;
# }})()"""

class GIf:
    def __init__(self, cond, value):
        self.cond = cond
        self.value = value

    def to_js(self):
        val = self.value.to_h()
        return f"if ({self.cond}) return {val};"


class GElse:
    def __init__(self, value):
        self.value = value

    def to_js(self):
        val = self.value.to_h()
        return f"else return {val};"

class Node:
    """Base class for all AST nodes"""
    pass


class JSNode(Node):
    """Anything that outputs RAW JS"""
    def to_h(self):
        raise NotImplementedError

class G:
    def __init__(self, *branches):
        self.branches = branches
        self.type = "element"

    def to_h(self):
        lines = [b.to_js() for b in self.branches]
        body = "\n".join(lines)

        return f"(()=> {{\n{body}\n}})()".strip()




@Component
@view
def homePage():
    req = useRequest(
        url="https://jsonplaceholder.typicode.com/posts/1",
        method="GET",
        headers={
            "Authorization": "Bearer TOKEN123"
        }
    )

    count = Create(1)

    return CreateElement(
        "div",
        {},
        CreateElement("h1", {}, "Home Page"),
        CreateElement("p", {}, f"{count.get()}"),
        CreateElement("p", {}, f"{req.get('title')}"),

        G(
            GIf(
                f"{count.get()} < 5",
                CreateElement("p", {}, "Number is less than 5")
            ),
            GIf(
                f"{count.get()} < 10",
                CreateElement("p", {}, "Number is between 5 and 8")
            ),
            GElse(
                CreateElement("p", {}, "Number is 10 or more")
            )
        ),

        CreateElement(
            "button",
            {"on:click": count.set(lambda c: c + 1)},
            "+1"
        )
    )


fetch = Fetch("https://jsonplaceholder.org/posts/1")
post_1 = fetch.get("name")

router.render('/', homePage())

router.run('root')
doc.build()
