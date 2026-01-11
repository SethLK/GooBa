import inspect

from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest, GIf, GElse, G, GELIf

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

        G(
            GIf(
                count.value() < 5,
                CreateElement("p", {}, "Number is less than 5")
            ),
            GELIf(
                count.value() > 5,
                CreateElement("p", {}, "Number is between 5 and 8")
            ),
            GElse(
                CreateElement("p", {}, "Number is 10 or more")
            )
        ),

        CreateElement(
            "button",
            {"on:click": count.set(lambda c: c + 1)},
            "+1"
        )
    )


fetch = Fetch("https://jsonplaceholder.org/posts/1")
post_1 = fetch.get("name")

router.render('/', homePage())

router.run('root')
doc.build()
