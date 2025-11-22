
def user_page():
    return (
CreateElement(
    'div',
    {},
    CreateElement(
        'p',
        {},
        ' Hello There '
    ),
    '',
    CreateElement(
        'div',
        {"class": "container"},
        CreateElement(
            'h1',
            {},
            ' Hello There '
        ),
        '',
    ),
    '',
)
)