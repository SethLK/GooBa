import { signal } from "./reactive/signal.js";
import { effect } from "./reactive/effect.js";
import { h, hFragment, hString } from "./h.js";
import { mountDOM, type VNode } from "./dom/mount-dom.js";
import { destroyDOM } from "./dom/destroy-dom.js";
import { Dispatcher } from "./dispatcher.js";

export type Reducer<T> = (state: T, payload: any) => T;

export type Emit = (eventName: string, payload?: any) => void;

export type AppOptions<T> = {
  state: T;
  view: (state: T, emit: Emit) => VNode;
  reducers?: Record<string, Reducer<T>>;
};

export function createApp<T>({ state, view, reducers = {} }: AppOptions<T>) {
  let parentEl: HTMLElement | null = null;
  let vdom: VNode | null = null;

  const dispatcher = new Dispatcher<string>();

  const subscriptions = [dispatcher.after(renderApp)]
  const emit: Emit = (eventName, payload) => {
    dispatcher.dispatch(eventName, payload);
  };

  for (const actionName in reducers) {
    const reducer = reducers[actionName];
    if (!reducer) continue; 
    const unsub = dispatcher.subscribe(actionName, (payload) => {
      state = reducer(state, payload);
    });
    subscriptions.push(unsub);
  }

  function renderApp() {
    if (vdom) destroyDOM(vdom);

    vdom = view(state, emit);

    if (parentEl) {
      mountDOM(vdom, parentEl);
    }
  }

  return {
    mount(_parentEl: HTMLElement) {
      parentEl = _parentEl;
      renderApp();
    },

    unmount() {
      if (vdom) destroyDOM(vdom);
      subscriptions.forEach((unsub) => unsub());
    },
  };
}

export { signal, effect, h, mountDOM, hString, destroyDOM, Dispatcher, hFragment }
export type { VNode };
