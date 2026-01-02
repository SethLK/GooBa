
import { destroyDOM } from "./destroy-dom.js";
import { h, hFragment, hString } from "./h.js";
import { runWithHooks, Create, withHooks } from "./hooks.js";
import { mountDOM, type VNode } from "./mount-dom.js";
import { varState } from "./state.js";

let scheduleRender: (() => void) | null = null;

export type AppOptions<T> = {
    state: T;
    view: (state: T) => VNode;
};

export function createApp<T>({ state, view }: AppOptions<T>) {
    let parentEl: HTMLElement | null = null;
    let vdom: VNode | null = null;

    const hookedView = withHooks(view);

    function renderApp() {
        if (vdom) destroyDOM(vdom);

        // Run inside hook context
        vdom = runWithHooks(hookedView as any, () => hookedView(state));

        if (parentEl) {
            mountDOM(vdom, parentEl);
        }
    }

    scheduleRender = renderApp;

    return {
        // mount(_parentEl: HTMLElement) {
        //     parentEl = _parentEl;
        //     renderApp();
        // },
        mount(_parentEl: HTMLElement) {
            parentEl = _parentEl;
            parentEl.innerHTML = "";   // <-- clear previous DOM
            renderApp();
        },


        unmount() {
            if (vdom) destroyDOM(vdom);
        },
    };
}

export function triggerRender() {
    if (scheduleRender) scheduleRender();
}


function useRequest<T = unknown>(baseHeaders: HeadersInit = {}) {
  const data = Create<T | null>(null);
  const loading = Create(false);
  const error = Create<Error | null>(null);

  const request = async (
    url: string,
    options: RequestInit = {}
  ): Promise<T> => {
    loading.set(true);
    error.set(null);

    try {
      const res = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...baseHeaders,
          ...(options.headers ?? {})
        }
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const json = (await res.json()) as T;
      data.set(json);
      return json;
    } catch (err) {
      error.set(err as Error);
      throw err;
    } finally {
      loading.set(false);
    }
  };

  return { data, loading, error, request };
}

export { useRequest };


export {
    Create, h, mountDOM, hString, destroyDOM, hFragment, varState, varState as state, runWithHooks, withHooks
};
export type { VNode };