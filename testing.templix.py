
from GooBa import view, CreateElement, Fetch

@view
def another():
    return (
        <div>
        <h1>Title - ${ctx.params.title}</h1>
        <p>Content - ${ctx.params.content}</p>

        </div>
    )

@view
def another_2():
    return (
        <div>
        <h2> HTML Forms </h2>
        <form action="/">
        <label for ="title"> First name: </label> <br>
        <input type="text" id="title" name="title" value="Something" /> <br/>
        <label for ="content"> Last name: </label> <br>
        <input type="text" id="content" name="content" value="Doe" /> <br/> <br/>
        <input type="submit" value="Submit" />
        </form>
        <p> If you click the "Submit" button, the form-data will be sent to a page called </p>
        </div>
    )