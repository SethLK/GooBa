import inspect

from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest, GIf, GElse, G, GELIf, Loop, Fragment
from GooBa.Extern import Event, event

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

    items = Create([
        {"name": "Molecule Man", "age": 29},
        {"name": "Madame Uppercut", "age": 39},
        {"name": "Eternal Flame", "age": 1000000}
    ])

    newItem = Create("")
    age = Create(0)

    req = useRequest(
        url="http://localhost:8080/something.json",
        method="GET",
    )

    count = Create(1)
    # print(req.value())
    # lc = lambda e: newItem.set(e.target.value)
    # print(lc(''))

    return CreateElement(
        "div",
        {},
        CreateElement("h1", {}, "Home Page"),
        CreateElement("p", {}, f"{count.get()}"),
        # CreateElement("p", {}, f"{req.get('name')}"),


    #     h("input", {
    #   type: "text",
    #   placeholder: "New item name",
    #   value: newItem.get(),
    #   on: {
    #     input: (e) => newItem.set(e.target.value)
    #   },
    # }),
    # h("button", {
    #   on: { click: () => {
    #     if (newItem.get().trim() !== '') {
    #       items.set([...items.get(), { name: newItem.get(), age: 0 }]);
    #       newItem.set('');
    #     }
    #   } }
    # }, ["Add Item"]),
    #
        CreateElement("input",
                      {
                          "type": "text",
                          "placeholder": "New item name",
                          "value": newItem.value(),
                          "on:input": newItem.set(event.target.value)
                      }
                      ),
        CreateElement("button", {
            "on:click": items.set(
                f"[...{items.value()}, {{ name: {newItem.value()}, age: {age.value()} }}]"
            )
        }, "Add Item"),


        CreateElement(
            "div",
            {},
            Loop(
                          items.value(),
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

router.render('/', homePage())

router.run('root')
doc.build()
