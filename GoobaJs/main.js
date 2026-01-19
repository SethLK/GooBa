
import { createApp, h, Create, withHooks, useRequest, useOnce, hFragment } from "/dist/gooba.js";
function render(componentFn) {
  createApp({ view: componentFn }).mount(document.getElementById("root"));
}


// Static routes

page('/', () => {
  render(function HomePage() {
    const fetch0 = useRequest();
    useOnce(() => {
      fetch0.request("http://localhost:8080/something.json", {
        method: "GET"
      });
    });
    const state0 = Create([{ 'name': 'Molecule Man', 'age': 29 }, { 'name': 'Madame Uppercut', 'age': 39 }, { 'name': 'Eternal Flame', 'age': 1000000 }]);
    const state1 = Create([{ 'name': 'Molecule Man', 'age': 29 }, { 'name': 'Madame Uppercut', 'age': 39 }, { 'name': 'Eternal Flame', 'age': 1000000 }]);
    const state2 = Create();
    const state3 = Create(1);
    return h("div", {}, [
      h("h1", {}, [
        `Home Page`
      ]),
      h("p", {}, [
        `${state3.get()}`
      ]),
      h("input", 
        { type: "text", 
          placeholder: "New item name", 
          value: state2.get(), on: { input: (e) => newItem.set(e.target.value) }}),
      h("button", { on: { click: () => state1.set(`[...state1.get(), { name: state2.get(), age: 0 }]`) } }, [
        `Add Item`
      ]),
      h("div", {}, [
        ...fetch0.data.get()?.map(item => hFragment([h("h3", {}, [
          `${item.name}`
        ]), h("p", {}, [
          `Age: ${item.age}`
        ])])) ?? []
      ]),
      h("button", { on: { click: () => state3.set(c => c + 1) } }, [
        `+1`
      ])
    ]);
  });
});


// Dynamic routes


// 404 handler
page('*', () => {
  render('<h2>404 Page Not Found</h2>');
});

page.start();