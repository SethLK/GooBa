from GooBa.Templix import view, Component
from GooBa import CreateElement



def main_page():
    return (
        CreateElement(
            'div',
            {},
            '',
            CreateElement(
                'img',
                {
                    'src': 'https://www.w3schools.com/html/pic_trulli.jpg',
                },
            ),
            '',
        )
    )


def main_page2():
    return (
        CreateElement(
            'div',
            {},
            '',
            CreateElement(
                'p',
                {},
                'Hello There',
            ),
            '',
            CreateElement(
                'div',
                {
                    'class': 'container',
                },
                '',
                CreateElement(
                    'h1',
                    {},
                    ' Hello There',
                ),
                '',
            ),
            '',
        )
    )



def main_page337():
    return (
        CreateElement(
            'div',
            {},
            '',
            CreateElement(
                'p',
                {},
                'Hello There',
            ),
            '',
            CreateElement(
                'div',
                {
                    'class': 'container',
                },
                '',
                CreateElement(
                    'h1',
                    {},
                    ' Hello There',
                ),
                '',
            ),
            '',
        )
    )


def user_page():
    return (
        CreateElement(
            'div',
            {},
            '',
            CreateElement(
                'p',
                {},
                ' Hello There ',
            ),
            '',
            CreateElement(
                'div',
                {
                    'class': 'container',
                },
                '',
                CreateElement(
                    'h1',
                    {},
                    ' Hello There ',
                ),
                '',
            ),
            '',
        )
    )