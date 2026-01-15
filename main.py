import inspect

from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest, GIf, GElse, G, GELIf, Loop, Fragment

doc = Document()
router = Router()

@Component
@view
def homePage():

    data = Create(
        [
            {"name": "Molecule Man", "age": 29},
            {"name": "Madame Uppercut", "age": 39},
            {"name": "Eternal Flame", "age": 1000000}
        ]
    )
    req = useRequest(
        url="http://localhost:8080/something.json",
        method="GET",
    )

    count = Create(1)
    # print(req.value())

    return CreateElement(
        "div",
        {},
        CreateElement("h1", {}, "Home Page"),
        CreateElement("p", {}, f"{count.get()}"),
        # CreateElement("p", {}, f"{req.get('name')}"),

        CreateElement(
            "div",
            {},
            Loop(
                          req.value(),
                          lambda hero: Fragment(
                              CreateElement("h3", {}, f"{hero.get('name')}"),
                              CreateElement("p", {}, f"Age: {hero.get('age')}")
                          ),
            ),
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
