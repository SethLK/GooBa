
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
        <form action="/action_page.php">
        <label for ="fname"> First name: </label> <br>
        <input type="text" id="fname" name="fname" value="John" /> <br/>
        <label for ="lname"> Last name: </label> <br>
        <input type="text" id="lname" name="lname" value="Doe" /> <br/> <br/>
        <input type="submit" value="Submit" />
        </form>
        <p> If you click the "Submit" button, the form-data will be sent to a page called </p>
        </div>
    )