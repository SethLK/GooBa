import { createApp, h, Create, withHooks } from "./dist/gooba.js";

const postData = {
  title: 'My New Post',
  body: 'This is the content of my new post.',
  userId: 1,
};

function submit() {

  fetch('https://jsonplaceholder.typicode.com/posts', {
    method: 'POST', // Specify the method
    headers: {
      'Content-Type': 'application/json', // Indicate the body format
    },
    body: JSON.stringify(postData), // Convert the JavaScript object to a JSON string
  })
    .then(response => {
      // Check if the request was successful (status code 200-299)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // Parse the JSON response body
    })
    .then(data => {
      console.log('Success:', data); // Log the response data from the server
    })
    .catch((error) => {
      console.error('Error:', error); // Handle any errors during the fetch operation
    });
}



// --- Components ---
export function AppHome() {
  const count = Create(0);
  return h("div", {}, [
    h("h1", {}, ["Home Page"]),
    h("button", { on: { click: () => count.set(c => c + 1) } }, ["+1"]),
    h("p", {}, [`Count: ${count.get()}`]),
    h("button", {
      on: {
        click: () => submit()
      }
    }, ["Submit"]),
    h("a", { href: "/product" }, ["Go to Product"]),
    h("a", { href: "/param/123" }, ["Go to Param with ID 123"]),
    h("a", { href: "/param/456" }, ["Go to Param with ID 456"]),
    h("a", { href: "/not-found" }, ["Go to Not Found"])
  ]);
}

function useFetch(url) {
  const data = Create(null);
  const loading = Create(true);
  const error = Create(null);

  fetch(url)
    .then(r => r.json())
    .then(json => data.set(json))
    .catch(err => error.set(err))
    .finally(() => loading.set(false));

  return { data, loading, error };
}

function Card(props) {
  return h("div", {}, [
    h("h1", {}, [`${props.title}`]),
    h("p", {}, [`Param ID: ${props.id}`]),
    h("p", {}, [`Param ID: ${props.description}`]),
  ]);
}


export function AppProduct() {
  const count = Create(0);
  const data = Create(null);
  const loading = Create(true);
  const error = Create(null);


  const fetchData = async () => {
    try {
      const response = await fetch("https://dummyjson.com/products/1");
      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      const result = await response.json();
      data.set(result);
    } catch (err) {
      error.set(err);
    } finally {
      loading.set(false);
    }
  };

  fetchData();
  // const { data, loading, error } = useFetch("https://dummyjson.com/products/1");

  return h("div", {}, [
    h("h1", {}, ["Product Page"]),
    h("button", { on: { click: () => count.set(c => c + 1) } }, ["+1"]),
    h("p", {}, [
      loading.get()
        ? "Loading..."
        : error.get()
          ? `Error: ${error.get().message}`
          : Card({
            title: data.get().title,
            id: data.get().id,
            description: data.get().description
          })
    ]),
    h("p", {}, [`Count: ${count.get()}`]),
    h("a", { href: "/" }, ["Back Home"])
  ]);
}

export const NotFound = withHooks(function NotFound() {
  return h("h2", {}, ["404 Page Not Found"]);
});

export function Param(props) {
  return h("div", {}, [
    h("h1", {}, ["Param Page"]),
    h("p", {}, [`Param ID: ${props.id}`]),
    h("a", { href: "/" }, ["Back Home"])
  ]);
};


function render(componentFn) {
  createApp({ view: componentFn }).mount(document.getElementById("root"));
}

// page("/", () => render(AppHome));      // ✔ pass function
page('/', () => {
  render(function HomePage() {
    const state0 = Create(0);
    return h("div", {}, [
      h("h1", {}, [
        `Home Page`
      ]),
      h("p", {}, [
        `${state0.get()}`
      ]),
      h("button", { onclick: () => state0.set(c => c + 1) }, [
        `+1`
      ])
    ]);
  });
});

page("/product", () => render(AppProduct));
page("/param/:id", (ctx) => render(() => Param({ id: ctx.params.id })));


page("*", () => render(NotFound));


page.start();
