from GooBa.Templix import view, Component
from GooBa import CreateElement

class ShareLink(Component):
    def render(self):
        return <a href={self.props['link']}>Share on internet</a>

@view
def tag():
    share = "https://example.com"
    return <ShareLink link={share} />

@view
def main_page():
    return (
        <div>
        <h1>Hello WOrld</h1>
        </div>
    )