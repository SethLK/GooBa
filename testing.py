
from GooBa import view, CreateElement, Fetch

@view
def another():
    return (
CreateElement(
    "div",
    {  },
    CreateElement(
        "h1",
        {  },
        "Title - ${ctx.params.title}"
    ),
    CreateElement(
        "p",
        {  },
        "Content - ${ctx.params.content}"
    )
)
)

@view
def another_2():
    return (
CreateElement(
    "div",
    {  },
    CreateElement(
        "h2",
        {  },
        "HTML Forms"
    ),
    CreateElement(
        "form",
        { "action": "/" },
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
            { "type": "text", "id": "title", "name": "title", "value": "Something" },
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
            { "type": "text", "id": "content", "name": "content", "value": "Doe" },
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
            "input",
            { "type": "submit", "value": "Submit" },
            ""
        )
    ),
    CreateElement(
        "p",
        {  },
        "If you click the \"Submit\" button, the form-data will be sent to a page called"
    )
)
)