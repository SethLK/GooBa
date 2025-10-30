import functools
import inspect
import re
import sys
from typing import Any

from pyPEG import attr, optional, name, List, ignore, maybe_some, Symbol, parse, compose


class TemplatePlaceholder(object):
    """Matches {{{expr}}} and turns it into '{{expr}}' literal (for routers/templates)."""

    grammar = '{{{', attr('expr', re.compile(r'[^}]+')), '}}}'

    def __init__(self):
        self.expr = None

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        # return a literal '{{expr}}' string
        return "{indent}'{{{{{expr}}}}}'".format(
            indent=indent_str,
            expr=self.expr.strip()
        )

# class RawPlaceholder(object):
#     """Matches triple braces {{{expr}}} and outputs them as-is."""
#
#     grammar = '{{{', attr('expr', re.compile(r'[^}]+')), '}}}'
#
#     def compose(self, parser, indent=0):
#         indent_str = indent * "    "
#         # output exactly what was typed
#         return "{indent}{{{{{{{expr}}}}}}}".format(
#             indent=indent_str,
#             expr=self.expr.strip()
#         )

class RawPlaceholder(object):
    """Matches triple braces {{{expr}}} and outputs them exactly as written."""

    grammar = '{{{', attr('expr', re.compile(r'[^}]+')), '}}}'

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        # output exactly: {{{expr}}}
        return f"{indent_str}{{{{{{{{{self.expr.strip()}}}}}}}}}"

class RawBracesText(object):
    """Treat any {...}, {{...}}, or {{{...}}} as plain text — no parsing, no changes."""

    grammar = attr('content', re.compile(r'\{+[^}]+\}+'))

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return f"{indent_str}{repr(self.content)}"


whitespace = re.compile(r"\s+")
text = re.compile(r'[^<]+')

VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr',
    'img', 'input', 'link', 'meta', 'param',
    'source', 'track', 'wbr'
}

class Whitespace(object):
    """Matches one or more whitespace characters

    When composing we compress runs of whitespace to a single space in the
    generated Python source (this mirrors original behaviour).
    """

    grammar = attr('value', whitespace)

    def compose(self, parser, indent=0):
        # Return a python literal that represents a single space between tokens.
        indent_str = indent * "    "
        return "{indent}''".format(indent=indent_str)


class Text(object):
    """Matches text between tags and/or inline code sections."""

    grammar = attr('whitespace', optional(whitespace)), attr('value', re.compile(r"[^<{]+"))

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        ws = self.whitespace or ''
        # Escape single quotes in the composed python string literal
        safe_value = self.value.replace("'", "\\'")
        return "{indent}'{whitespace}{value}'".format(
            indent=indent_str,
            whitespace=ws,
            value=safe_value
        )


class String(object):
    """Matches a double-quote delimited string."""

    grammar = '"', attr('value', re.compile(r'[^"]*')), '"'

    def compose(self, parser):
        # Return a Python single-quoted literal
        safe = self.value.replace("'", "\\'")
        return "'%s'" % safe


class InlineCode(object):
    """Matches arbitrary Python code within curly braces."""

    grammar = '{', attr('code', re.compile(r'[^}]*')), '}'

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}{code}".format(
            indent=indent_str,
            code=self.code
        )


class Attribute(object):
    """Matches an attribute formatted as either: key="value" or key={value}.

    Value is stored as either a String or InlineCode instance. compose() will
    call the nested compose when necessary.
    """

    grammar = name(), '=', attr('value', [String, InlineCode])

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        # value may be an object with compose() or a raw string
        val = self.value
        if hasattr(val, 'compose'):
            value_code = val.compose(parser)
        else:
            # fallback: treat as raw
            value_code = repr(val)

        return "{indent}'{name}': {value},".format(
            indent=indent_str,
            name=self.name,
            value=value_code
        )


class Attributes(List):
    """Matches zero or more attributes"""

    grammar = optional(ignore(Whitespace), Attribute, maybe_some(ignore(Whitespace), Attribute))

    def compose(self, parser, followed_by_children, indent):
        indent_str = indent * "    "

        if not len(self):
            # no attributes: return empty dict literal only if children will follow
            return '{indent}{{}},\n'.format(indent=indent_str) if followed_by_children else ''

        parts = []
        parts.append('{indent}{{\n'.format(indent=indent_str))
        for entry in self:
            if not isinstance(entry, str):
                parts.append(entry.compose(parser, indent=indent+1))
                parts.append('\n')
        parts.append('{indent}}},\n'.format(indent=indent_str))

        return ''.join(parts)


class SelfClosingTag(object):
    """Matches a self-closing tag and all of its attributes."""

    grammar = '<', name(), attr('attributes', Attributes), ignore(whitespace), '/>'

    def get_name(self):
        return "'%s'" % self.name

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_contents = bool(self.attributes)
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}CreateElement({paren_sep}{indent_plus}{name}{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.get_name(),
                paren_sep=paren_sep,
                contents_sep=contents_sep,
            )
        )
        text.append(self.attributes.compose(parser, followed_by_children=False, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
            )
        )

        return ''.join(text)


class ComponentName(object):
    """A standard name or symbol beginning with an uppercase letter."""

    grammar = attr('first_letter', re.compile(r'[A-Z]')), attr('rest', optional(Symbol))

    def compose(self):
        return self.first_letter + (self.rest if self.rest else '')


class ComponentTag(SelfClosingTag):
    """Self-closing tag whose name starts with an uppercase letter; treated as a component."""

    grammar = (
        '<', attr('name', ComponentName), attr('attributes', Attributes), ignore(whitespace), '/>'
    )

    def get_name(self):
        return self.name.compose()


class PairedTag(object):
    # """Matches an open/close tag pair and all of its attributes and children."""
    #
    # @staticmethod
    # def parse(parser, text, pos):
    #     result = PairedTag()
    #     try:
    #         text, _ = parser.parse(text, '<')
    #         text, tag = parser.parse(text, Symbol)
    #         result.name = tag
    #         text, attributes = parser.parse(text, Attributes)
    #         result.attributes = attributes
    #         text, _ = parser.parse(text, '>')
    #         text, children = parser.parse(text, TagChildren)
    #         result.children = children
    #         text, _ = parser.parse(text, optional(whitespace))
    #         text, _ = parser.parse(text, '</')
    #         text, _ = parser.parse(text, result.name)
    #         text, _ = parser.parse(text, '>')
    #     except SyntaxError as e:
    #         return text, e
    #
    #     return text, result

    """Matches an open/close tag pair and all of its attributes and children."""

    VOID_TAGS = {
        'area', 'base', 'br', 'col', 'embed', 'hr',
        'img', 'input', 'link', 'meta', 'param',
        'source', 'track', 'wbr'
    }

    @staticmethod
    def parse(parser, text, pos):
        result = PairedTag()
        try:
            # Opening tag
            text, _ = parser.parse(text, '<')
            text, tag = parser.parse(text, Symbol)
            result.name = tag
            text, attributes = parser.parse(text, Attributes)
            result.attributes = attributes

            # Self-closing check
            text, maybe_closer = parser.parse(text, optional('/'))
            text, _ = parser.parse(text, '>')

            # ✅ Handle void/self-closing tags
            if result.name.lower() in PairedTag.VOID_TAGS or maybe_closer:
                result.children = []
                return text, result

            # Normal paired tag
            text, children = parser.parse(text, TagChildren)
            result.children = children
            text, _ = parser.parse(text, optional(whitespace))
            text, _ = parser.parse(text, '</')
            text, _ = parser.parse(text, result.name)
            text, _ = parser.parse(text, '>')

        except SyntaxError as e:
            return text, e

        return text, result

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_children = bool(self.children)
        has_attributes = bool(self.attributes)
        has_contents = has_children or has_attributes
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}CreateElement({paren_sep}{indent_plus}'{name}'{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.name,
                paren_sep=paren_sep,
                contents_sep=contents_sep
            )
        )
        text.append(
            self.attributes.compose(parser, followed_by_children=has_children, indent=indent+1)
        )
        if self.children:
            text.append(self.children.compose(parser, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
            )
        )

        return ''.join(text)


# The set of possible tag types we accept
tags = [ComponentTag, PairedTag, SelfClosingTag]


class TagChildren(List):
    """Matches valid tag children which can be other tags, plain text, {values} or a mix of all
    three."""

    # grammar = maybe_some(tags + [Text, InlineCode, Whitespace])
    # grammar = maybe_some(tags + [Text, InlineCode, RawPlaceholder, Whitespace])
    grammar = maybe_some(tags + [Text, InlineCode, RawBracesText, Whitespace])


    def compose(self, parser, indent=0):
        text = []
        for entry in self:
            text.append(entry.compose(parser, indent=indent))
            text.append(',\n')

        return ''.join(text)


class PackedBlock(List):
    """Matches multi-line block of Packed syntax where the syntax starts on the first line"""

    grammar = attr('line_start', re.compile(r'[^#<\n]+')), tags

    def compose(self, parser, attr_of=None):
        text = [self.line_start]
        indent_text = re.match(r' *', self.line_start).group(0)
        indent = int(len(indent_text) / 4)
        for entry in self:
            if isinstance(entry, str):
                text.append(entry)
            else:
                text.append(entry.compose(parser, indent=indent, first=True))

        return ''.join(text)


class NonPackedLine(List):
    """Match a normal python line (no packed syntax) including its newline."""

    grammar = attr('content', re.compile('.*')), '\n'

    def compose(self, parser, attr_of=None):
        return '%s\n' % self.content


line_without_newline = re.compile(r'.+')


class CodeBlock(List):
    """Top level grammar representing a block of code, some of which will be Packed syntax and some
    won't.
    """

    grammar = maybe_some([PackedBlock, NonPackedLine, line_without_newline])

    def compose(self, parser, attr_of=None):
        parts = []
        for entry in self:
            if isinstance(entry, str):
                parts.append(entry)
            else:
                parts.append(entry.compose(parser))

        return ''.join(parts)


# ------------------------- Rendering helpers ---------------------------------

def format_attribute(key, value):
    """Handles the output format for an attribute to the final html"""
    return '{name}="{value}"'.format(name=key, value=value)


def to_html(entity: Any) -> str:
    """Converts entity to output html with the ability to handle Elem instances & strings and lists."""

    if isinstance(entity, (list, tuple)):
        return ''.join(map(to_html, entity))

    if hasattr(entity, 'to_html'):
        return entity.to_html()
    else:
        return str(entity)


class Elem(object):
    """Represents an HTML element. Packed translates the <a></a> into Elem('a') with an optional
    dictionary argument for attributes and further arguments being children.

    Provides a to_html method for recursively outputting the final html.
    """

    def __init__(self, name, attributes=None, *children):

        self.name = name
        self.attributes = attributes or {}
        self.children = children

    def to_html(self):

        # Handle components by instantiating them and calling their render method
        if inspect.isclass(self.name):
            assert not self.children
            instance = self.name(**self.attributes)

            output = instance.render()

            return to_html(output)

        attribute_text = ''
        if self.attributes:
            attribute_text = ' '.join(
                map(
                    lambda item: format_attribute(item[0], item[1]),
                    self.attributes.items()
                )
            )

        if attribute_text:
            attribute_text = ' ' + attribute_text

        children_text = ''
        if self.children:
            children_text = ''.join(map(to_html, self.children))
        return "<{name}{attributes}>{children}</{name}>".format(
            name=self.name,
            attributes=attribute_text,
            children=children_text
        )


class Component(object):
    """Simple component base class that exposes incoming attributes in self.props similar to React."""

    def __init__(self, **props):
        self.props = props

    def render(self):
        raise NotImplementedError


def view(func):
    """Decorator for functions that return Elem trees. The wrapper renders to HTML string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        text = to_html(result)
        return text

    return wrapper

# def clean_html_like(code: str) -> str:
#     # Step 1: Collapse all newlines and extra spaces
#     code = re.sub(r'\s+', ' ', code)
#
#     # Step 2: Remove unnecessary spaces around angle brackets
#     code = re.sub(r'\s*<\s*', '<', code)
#     code = re.sub(r'\s*>\s*', '>', code)
#     code = re.sub(r'\s*<\s*/\s*', '</', code)
#
#     # Step 3: Fix attribute spacing (class ="x" → class="x")
#     code = re.sub(r'\s*=\s*', '=', code)
#
#     # Step 4: Restore some readable indentation (optional)
#     tokens = re.findall(r'<[^>]+>|[^<]+', code)
#     indent = 0
#     formatted = []
#
#     for token in tokens:
#         token = token.strip()
#         if not token:
#             continue
#
#         if token.startswith('</'):
#             indent -= 1
#         formatted.append('    ' * indent + token)
#         if token.startswith('<') and not token.startswith('</') and not token.endswith('/>'):
#             if not token.startswith('<!') and not token.startswith('<?'):
#                 indent += 1
#
#     return '\n'.join(formatted)


# def clean_html_like(code: str) -> str:
#     """
#     Cleans unnecessary spaces in HTML-like syntax inside mixed Python/HTML code
#     without damaging indentation, strings, or Python structure.
#     """
#
#     def clean_tag(match):
#         tag = match.group(0)
#         # Remove spaces inside angle brackets like < div > → <div>
#         tag = re.sub(r'<\s+', '<', tag)
#         tag = re.sub(r'\s+>', '>', tag)
#         tag = re.sub(r'\s*=\s*', '=', tag)
#         tag = re.sub(r'\s*/\s*>', '/>', tag)
#         return tag
#
#     # Step 1: Only clean tags, not entire file
#     code = re.sub(r'<[^>]+>', clean_tag, code)
#
#     # Step 2: Remove extra spaces *between* HTML tags only
#     code = re.sub(r'>\s+<', '><', code)
#
#     # Step 3: Restore consistent indentation for tags (optional)
#     tokens = re.findall(r'<[^>]+>|[^\n<]+', code)
#     indent = 0
#     formatted = []
#
#     for token in tokens:
#         stripped = token.strip()
#         if not stripped:
#             continue
#
#         if stripped.startswith('</'):
#             indent -= 1
#
#         if stripped.startswith('<'):
#             formatted.append('    ' * indent + stripped)
#             if not stripped.startswith('</') and not stripped.endswith('/>'):
#                 indent += 1
#         else:
#             # Keep Python code or text as-is
#             formatted.append('    ' * indent + stripped)
#
#     return '\n'.join(formatted)

# def clean_html_whitespace(code: str) -> str:
#     # Remove spaces after '<' (e.g., "< div" → "<div")
#     code = re.sub(r'<\s+', '<', code)
#     # Remove spaces before '>' (e.g., "div >" → "div>")
#     code = re.sub(r'\s+>', '>', code)
#     code = re.sub(r'<\s*/\s*', '</', code)
#
#     return code.strip()

# def clean_html_whitespace(code: str) -> str:
#     def fix_tag(match):
#         tag = match.group(0)
#         tag = re.sub(r'<\s+', '<', tag)
#         tag = re.sub(r'\s+>', '>', tag)
#         tag = re.sub(r'<\s*/\s*', '</', tag)
#         return tag
#
#     # only fix inside <...>
#     return re.sub(r'<[^>]+>', fix_tag, code)

def clean_html_whitespace(code: str) -> str:
    """
    Normalize HTML-like syntax so that extra spaces inside tags don't break parsing.
    e.g. < div class ="x" > → <div class="x">
    """

    def fix_tag(match):
        tag = match.group(0)

        # Remove space after '<' and before '>'
        tag = re.sub(r'<\s+', '<', tag)
        tag = re.sub(r'\s+>', '>', tag)

        # Fix spaces in closing tags: < /div > → </div>
        tag = re.sub(r'<\s*/\s*', '</', tag)

        # Fix spaces around '=' in attributes
        tag = re.sub(r'\s*=\s*', '=', tag)

        # Fix spaces in self-closing tags: <br / > → <br/>
        tag = re.sub(r'\s*/\s*>', '/>', tag)

        return tag

    # Apply cleanup to every <...> block
    return re.sub(r'<[^>]+>', fix_tag, code)




# def translate(code: str) -> str:
#     """Translate a single multi-line block of code from Packed syntax to valid Python."""
#     code = re.sub(r'<\s+/', '</', re.sub(r'<\s+', '<', code))
#     result = parse(code, CodeBlock, whitespace=None)
#     return compose(result)


def translate(code: str) -> str:
    """Translate a single multi-line block of code from Packed syntax to valid Python."""
    clean_code = clean_html_whitespace(code)
    result = parse(clean_code, CodeBlock, whitespace=None)
    return compose(result)


def translate_file(templix: str, py_path: str) -> None:
    with open(templix, 'r', encoding='utf-8') as fh:
        pkd_contents = fh.read()

    try:
        py_contents = translate(pkd_contents)
        py_contents = py_contents.replace("@view\n", "\n")
    except SyntaxError:
        sys.stderr.write('Failed to convert: %s\n' % templix)
        return

    with open(py_path, 'w', encoding='utf-8') as fh:
        fh.write(py_contents)
