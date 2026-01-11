import inspect


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

class Expr:
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code

    def to_js(self):
        return self.code

    def _bin(self, op, other):
        if isinstance(other, Expr):
            return Expr(f"{self.code} {op} {other.code}")
        return Expr(f"{self.code} {op} {other}")

    def __lt__(self, other): return self._bin("<", other)
    def __gt__(self, other): return self._bin(">", other)
    def __le__(self, other): return self._bin("<=", other)
    def __ge__(self, other): return self._bin(">=", other)
    def __eq__(self, other): return self._bin("==", other)
    def __ne__(self, other): return self._bin("!=", other)


# class GIf:
#     def __init__(self, cond, value):
#         source = inspect.getsource(cond)
#         source = source.replace("${", "").replace("}", "")
#         self.cond = source
#         self.value = value
#
#
#     def to_js(self):
#         val = self.value.to_h()
#         return f"if ({self.cond}) return {val};"

class GIf:
    def __init__(self, cond, value):
        if hasattr(cond, "to_js"):
            self.cond = cond.to_js()
        else:
            raise TypeError("GIf condition must be an expression")
        self.value = value

    def to_js(self):
        return f"if ({self.cond}) return {self.value.to_h()};"


class GELIf:
    def __init__(self, cond, value):
        if hasattr(cond, "to_js"):
            self.cond = cond.to_js()
        else:
            raise TypeError("GIf condition must be an expression")
        self.value = value

    def to_js(self):
        return f"else if ({self.cond}) return {self.value.to_h()};"


class GElse:
    def __init__(self, value):
        self.value = value

    def to_js(self):
        val = self.value.to_h()
        return f"else return {val};"
