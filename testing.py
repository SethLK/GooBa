
from GooBa import view, CreateElement, Fetch, Create, useRequest


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
    title = Create("")
    content = Create("")

    req = useRequest(
        url="http://localhost:3333/posts",
        method="POST",
        headers={"Content-Type": "application/json"},
        body={
            "title": title.value(),
            "content": content.value()
        }
    )
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
            { "type": "text", "id": "title", "name": "title", "value": "title.value()", "on:input": "title.set(event.target.value)" },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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
)           {  },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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
)           {  },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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
)           {  },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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
)           {  },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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
)           {  },
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
            { "type": "text", "id": "content", "name": "content", "value": "content.value()", "on:input": "content.set(event.target.value)" },
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