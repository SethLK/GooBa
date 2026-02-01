
from GooBa import view, CreateElement, Fetch, Create, useRequest


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
        <div>
        <h2> HTML Forms hi</h2>
        <form action="/">
        <label for ="title"> First name: </label> <br>
        <input type="text" id="title" name="title" value={title.value()} on:input= {title.set(event.target.value)}/> <br/>
        <label for ="content"> Last name: </label> <br>
        <input type="text" id="content" name="content" value={content.value()} on:input= {content.set(event.target.value)} /> <br/> <br/>
        <input type="submit" value="Submit" />
        </form>
        <p> If you click the "Submit" button, the form-data will be sent to a page called </p>
        </div>
    )