from GooBa.Templix import view, Component
from GooBa import CreateElement

class ShareLink(Component):
    def render(self):
        return CreateElement(
            'a',
            {
                'href': self.props['link'],
            },
            'Share on internet',
        )

@view
def tag():
    share = "https://example.com"
    return CreateElement(
        ShareLink,
        {
            'link': share,
        },
    )

@view
def main_page():
    return (
        CreateElement(
            'div',
            {},
            '',
            CreateElement(
                'h1',
                {},
                'Hello ',
                CreateElement('br'),
                ' WOrld',
            ),
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