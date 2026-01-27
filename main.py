import inspect

from GooBa import Document, CreateElement, Router, CreateStyle, Fetch, Create, Component, view, \
    Body, useRequest, GIf, GElse, G, GELIf, Loop, Fragment, Expr
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

# @Component
# def doing_Request():
#     req = useRequest(
#         url="http://localhost:3333/post",
#         method="POST",
#         headers={
#             "Content-Type": "application/json"
#         },
#         body={
#             "title": "Name",
#             "content": "Age"
#         }
#     )
#
#     return CreateElement(
#         "div",
#         {},
#         CreateElement("h1", {}, "Home Page"),
#         CreateElement(
#             "button",
#             {"on:click": req.trigger()},
#             "Add Item"
#         ),
#         G(
#             GIf(
#                 req.get("data"),
#                 CreateElement(
#                     "p",
#                     {},
#                     req.get("data")
#                 )
#             ),
#             GElse(
#                 CreateElement("p", {}, "Number is 10 or more")
#             )
#         )
#     )

@Component
def doing_Request():
    req = useRequest(
        url="http://localhost:3333/post",
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        body={
            "title": "Name",
            "content": "Age"
        }
    )

    return CreateElement(
        "div",
        {},
        CreateElement("h1", {}, "Home Page"),
        CreateElement(
            "button",
            {"on:click": req.trigger()},
            "Add Item"
        ),
        G(
            GIf(
                req.value(),
                CreateElement("p", {}, f"Request succeeded {req.get("message")}, {req.get("data.title")}")
            ),
            GElse(
                CreateElement("p", {}, "Waiting for response...")
            )
        )
    )

@Component
def doing_post_with_data():

    input_title = Create("")
    input_content = Create("")

    req = useRequest(
            url="http://localhost:3333/post",
            method="POST",
            headers={
                "Content-Type": "application/json"
            },
            body={
                "title": input_title.value(),
                "content": input_content.value()
            }
        )

    return CreateElement(
    "div",
    {  },
    CreateElement(
        "h2",
        {  },
        "HTML Forms"
    ),
    CreateElement(
        "form",
        { },
        CreateElement(
            "label",
            { "for": "title" },
            "First name:"
        ),
        CreateElement(
            "br",
            {  },
            ""
        ),
        CreateElement(
            "input",
            {
                "type": "text",
                "id": "title",
                "name": "title",
                "value": input_title.value(),
            "on:input": input_title.set(event.target.value)
            },
            ""
        ),
        CreateElement(
            "br",
            {  },
            ""
        ),
        CreateElement(
            "label",
            { "for": "content" },
            "Last name:"
        ),
        CreateElement(
            "br",
            {  },
            ""
        ),
        CreateElement(
            "input",
            {
                "type": "text",
                "id": "content",
                "name": "content",
                "value": input_content.value(),
                "on:input": input_content.set(event.target.value)
            },
            ""
        ),
        CreateElement(
            "br",
            {  },
            ""
        ),
        CreateElement(
            "br",
            {  },
            ""
        ),
        CreateElement(
                        "button",
                        {"on:click": req.trigger()},
                        "Add Item"
                    ),
    ),
    CreateElement(
        "p",
        {  },
        "If you click the \"Submit\" button, the form-data will be sent to a page called"
    )
)

router.render('/', doing_post_with_data())

router.run('root')
doc.build()
