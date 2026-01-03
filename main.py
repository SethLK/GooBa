
from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest

doc = Document()
router = Router()

@Component
@view
def homePage():
    req = useRequest(
        url="https://jsonplaceholder.typicode.com/posts/1",
        method="GET",
        headers={
            "Authorization": "Bearer TOKEN123"
        }
    )

    count = Create(1)

    return CreateElement(
        "div",
        {},
        CreateElement("h1", {}, "Home Page"),
        CreateElement("p", {}, f"{count.get()}"),
        CreateElement("p", {}, f"{req.get('title')}"),

        # Python ternary (JS ?: equivalent)
        CreateElement(
            "p",
            {},
            f"Count is small: {count.get()}"
        ) if (count.get() < 5) else CreateElement(
            "p",
            {},
            "Count is large"
        ),

        CreateElement(
            "button",
            {"on:click": lambda _: count.set(lambda c: c + 1)},
            "+1"
        )
    )


fetch = Fetch("https://jsonplaceholder.org/posts/1")
post_1 = fetch.get("name")

router.render('/', homePage())

router.run('root')
doc.build()
