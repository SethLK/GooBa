"""async function logMovies() {
  const response = await fetch("http://example.com/movies.json");
  const movies = await response.something.json();
  console.log(movies);
}"""


class Fetch:
    _id = 0

    def __init__(self, url):
        self.url = url
        self.id = Fetch._id
        Fetch._id += 1

    def to_js_init(self):
        return f"""
const fetch{self.id} = useRequest();
fetch{self.id}.request("{self.url}");
"""

    def get(self, key):
        return f"fetch{self.id}.data.get()?.{key}"

def Body(body):
    return (
        f"""JSON.stringify({body})"""
    )
