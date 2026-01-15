import inspect

from GooBa import Expr


class GFor:
    def __init__(self, condition):
        self.condition = condition


class GMap:
    def __init__(self):
        pass

class ForEach:
    def __init__(self, condition):
        self.condition = condition

class Fragment:
    def __init__(self, *children):
        self.children = list(children)

    def to_h(self):
        inner = ", ". join(child.to_h() for child in self.children)
        return inner


class Loop:
    def __init__(self, iterable, fn):
        self.iterable = iterable
        self.fn = fn

    def to_h(self):
        # 1. We define the name of the variable in JavaScript
        js_var_name = "item"

        # 2. We create a 'Proxy' Expr.
        # When the user calls hero.get('name'), this object returns "${item.name}"
        proxy = Expr(js_var_name)

        # 3. We EXECUTE the lambda in Python!
        # This returns a CreateElement object (or whatever your VNode is)
        vnode_result = self.fn(proxy)

        # 4. We convert that resulting VNode to its JavaScript string
        body_js = vnode_result.to_h() if hasattr(vnode_result, 'to_h') else str(vnode_result)

        # 5. Build the final map string
        iterable_js = self.iterable.to_js() if hasattr(self.iterable, 'to_js') else str(self.iterable)
        return f"...{iterable_js}?.map({js_var_name} => hFragment([{body_js}])) ?? []"

# class Loop:
#     def __init__(self, iterable, fn):
#         # if not hasattr(iterable, "to_js"):
#         #     raise TypeError("For expects an Expr as iterable")
#         self.iterable = iterable
#         self.fn = fn  # NOT executed now
#
#     def to_h(self):
#         global body
#         var = "item"
#         # body = self.fn(Expr(var)).to_h()
#         if callable(self.fn):
#             source = inspect.getsource(self.fn).strip()
#             # print(source)
#             start = source.find("lambda")
#             end = source.find(")}", start)
#
#             source = source[start:end]
#             source = source.replace("lambda", "").replace(":", " =>")
#             print(source)
#             body = source
#
#         if hasattr(self.fn, "to_h"):
#             print(self.fn.to_h())
#
#         print(f"{self.iterable}.map({var} => {body})")
#         return f"{self.iterable}.map({var} => {body})"

# h("ul", {}, items.get().map(item =>
#       h("li", {}, [`${item.name} (Age: ${item.age})`])
#     )),

# Loop(
#             req.value(),
#             lambda hero:
#                 CreateElement(
#                     "div", {},
#                     CreateElement("h3", {}, f"{hero.get('name')}"),
#                     CreateElement("p", {}, f"Age: {hero.get('age')}")
#                 )
#         ),

"""
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
        
        """