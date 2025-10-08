# jsx_parser.py
import ast
import re
from _ast import Constant, AST, Call
from typing import List, Union


class JSXTransformer(ast.NodeTransformer):
    def __init__(self):
        self.imports_needed = set()

    def visit_Expr(self, node):
        # Handle standalone JSX expressions
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            if self._is_jsx_like(node.value.value):
                parsed = self._parse_jsx(node.value.value)
                return ast.Expr(value=parsed)
        return self.generic_visit(node)

    def visit_Return(self, node):
        # Handle return statements with JSX
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            if self._is_jsx_like(node.value.value):
                parsed = self._parse_jsx(node.value.value)
                return ast.Return(value=parsed)
        return self.generic_visit(node)

    def _is_jsx_like(self, text: str) -> bool:
        """Check if string looks like JSX"""
        return text.strip().startswith('<') and text.strip().endswith('>')

    def _parse_jsx(self, jsx_string: str) -> ast.AST:
        """Convert JSX string to CreateElement calls"""
        return self._parse_element(jsx_string.strip())

    def _parse_element(self, element_str: str) -> Constant | AST:
        """Parse a single JSX element"""
        # Remove outer whitespace
        element_str = element_str.strip()

        if not element_str.startswith('<'):
            # This is text content
            return ast.Constant(value=element_str)

        # Handle self-closing tags first
        self_closing_match = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)\s*(.*?)\s*/>', element_str)
        if self_closing_match:
            tag_name = self_closing_match.group(1)
            attrs_str = self_closing_match.group(2)
            attrs = self._parse_attributes(attrs_str) if attrs_str else {}
            return self._create_element_call(tag_name, attrs, [])

        # Handle opening and closing tags
        open_tag_match = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)\s*(.*?)>', element_str)
        if not open_tag_match:
            raise ValueError(f"Invalid JSX: {element_str}")

        tag_name = open_tag_match.group(1)
        attrs_str = open_tag_match.group(2)
        attrs = self._parse_attributes(attrs_str) if attrs_str else {}

        # Find closing tag
        closing_tag = f"</{tag_name}>"
        content_start = open_tag_match.end()
        content_end = element_str.rfind(closing_tag)

        if content_end == -1:
            raise ValueError(f"Missing closing tag for {tag_name}")

        inner_content = element_str[content_start:content_end]
        children = self._parse_children(inner_content)

        return self._create_element_call(tag_name, attrs, children)

    def _parse_attributes(self, attrs_str: str) -> dict:
        """Parse attributes like href={url} class="btn" """
        attrs = {}
        # Simple regex for now - you can make this more robust
        attr_pattern = r'([a-zA-Z0-9_-]+)\s*=\s*(?:"([^"]*)"|{([^}]*)})'
        matches = re.findall(attr_pattern, attrs_str)

        for name, string_val, expr_val in matches:
            if string_val:
                attrs[name] = ast.Constant(value=string_val)
            elif expr_val:
                # Parse the expression inside {}
                try:
                    expr_ast = ast.parse(expr_val.strip(), mode='eval')
                    attrs[name] = expr_ast.body
                except SyntaxError:
                    # If it's not valid Python, treat as string
                    attrs[name] = ast.Constant(value=expr_val.strip())

        return attrs

    def _parse_children(self, content: str) -> List[ast.AST]:
        """Parse child elements and text"""
        if not content.strip():
            return []

        children = []
        i = 0
        while i < len(content):
            if content[i] == '<':
                # Find the end of this tag
                depth = 0
                j = i
                while j < len(content):
                    if content[j] == '<':
                        depth += 1
                    elif content[j] == '>':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1

                if j < len(content):
                    element_str = content[i:j + 1]
                    children.append(self._parse_element(element_str))
                    i = j + 1
                else:
                    # Invalid JSX, treat as text
                    children.append(ast.Constant(value=content[i:]))
                    break
            else:
                # Text content
                j = i
                while j < len(content) and content[j] != '<':
                    j += 1
                text = content[i:j].strip()
                if text:
                    children.append(ast.Constant(value=text))
                i = j

        return children

    def _create_element_call(self, tag_name: str, attrs: dict, children: List[ast.AST]) -> Call:
        """Create CreateElement call AST"""
        self.imports_needed.add('CreateElement')

        # Create keyword arguments for attributes
        keywords = []
        for attr_name, attr_value in attrs.items():
            keywords.append(ast.keyword(arg=attr_name, value=attr_value))

        # Create the call
        return ast.Call(
            func=ast.Name(id='CreateElement', ctx=ast.Load()),
            args=[ast.Constant(value=tag_name)] + children,
            keywords=keywords
        )


def transform_jsx_in_file(source_code: str) -> str:
    """Transform JSX-like syntax in Python source code"""
    try:
        tree = ast.parse(source_code)
        transformer = JSXTransformer()
        transformed_tree = transformer.visit(tree)

        # Add necessary imports
        if transformer.imports_needed:
            import_stmt = f"from GooBa import {', '.join(transformer.imports_needed)}"
            # Insert import at the beginning
            lines = import_stmt.split('\n') + ast.unparse(transformed_tree).split('\n')
            return '\n'.join(lines)
        else:
            return ast.unparse(transformed_tree)
    except Exception as e:
        print(f"JSX parsing error: {e}")
        return source_code