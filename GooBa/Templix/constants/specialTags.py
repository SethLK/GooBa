import re

VOID_ELEMENTS = [
	'area',
	'base',
	'br',
	'col',
	'embed',
	'hr',
	'img',
	'input',
	'keygen',
	'link',
	'menuitem',
	'meta',
	'param',
	'source',
	'track',
	'wbr',
]

NO_WHITESPACE = [
	'table',
	'tbody',
	'tfoot',
	'thead',
	'tr',
]

# Check if the tag is a void element (self-closing)
def can_have_children(tag_name: str) -> bool:
    """Return True if the tag can have child elements."""
    return tag_name.lower() not in VOID_ELEMENTS

# Check if the tag allows whitespace between elements
def can_have_whitespace(tag_name: str) -> bool:
    """Return True if the tag can have whitespace between elements."""
    return tag_name.lower() in NO_WHITESPACE

# Function to process HTML and add self-closing slashes to void elements
def add_self_closing_slash(html: str) -> str:
    # Regular expression pattern to match HTML tags
    tag_pattern = re.compile(r'<\s*(\w+)(.*?)\s*\/?>')

    def replace_tag(match):
        tag_name = match.group(1).lower()
        attributes = match.group(2).strip()

        # If it's a void element, ensure it has a self-closing slash
        if tag_name in VOID_ELEMENTS:
            # If it's already self-closing, leave it as is; else add '/'
            return f'<{tag_name}{attributes} />'
        else:
            # Otherwise, return the tag as is
            return match.group(0)

    # Use re.sub to replace tags in the HTML string
    return re.sub(tag_pattern, replace_tag, html)