from GooBa import view, CreateElement

@view
def Sompage():
    return (
CreateElement(
    "div",
    {  },
    CreateElement(
        "h2",
        {  },
        "HTML Tables"
    ),
    CreateElement(
        "p",
        {  },
        "HTML tables start with a table tag."
    ),
    CreateElement(
        "p",
        {  },
        "Table rows start with a tr tag."
    ),
    CreateElement(
        "p",
        {  },
        "Table data start with a td tag."
    ),
    CreateElement(
        "hr",
        {  },
        ""
    ),
    CreateElement(
        "h2",
        {  },
        "1 Column:"
    ),
    CreateElement(
        "table",
        {  },
        CreateElement(
            "tr",
            {  },
            CreateElement(
                "td",
                {  },
                "100"
            )
        )
    ),
    CreateElement(
        "hr",
        {  },
        ""
    ),
    CreateElement(
        "h2",
        {  },
        "1 Row and 3 Columns:"
    ),
    CreateElement(
        "table",
        {  },
        CreateElement(
            "tr",
            {  },
            CreateElement(
                "td",
                {  },
                "100"
            ),
            CreateElement(
                "td",
                {  },
                "200"
            ),
            CreateElement(
                "td",
                {  },
                "300"
            )
        )
    ),
    CreateElement(
        "hr",
        {  },
        ""
    ),
    CreateElement(
        "h2",
        {  },
        "3 Rows and 3 Columns:"
    ),
    CreateElement(
        "table",
        {  },
        CreateElement(
            "tr",
            {  },
            CreateElement(
                "td",
                {  },
                "100"
            ),
            CreateElement(
                "td",
                {  },
                "200"
            ),
            CreateElement(
                "td",
                {  },
                "300"
            )
        ),
        CreateElement(
            "tr",
            {  },
            CreateElement(
                "td",
                {  },
                "400"
            ),
            CreateElement(
                "td",
                {  },
                "500"
            ),
            CreateElement(
                "td",
                {  },
                "600"
            )
        ),
        CreateElement(
            "tr",
            {  },
            CreateElement(
                "td",
                {  },
                "700"
            ),
            CreateElement(
                "td",
                {  },
                "800"
            ),
            CreateElement(
                "td",
                {  },
                "900"
            )
        )
    ),
    CreateElement(
        "hr",
        {  },
        ""
    )
)
)