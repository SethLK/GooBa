
import { destroyDOM } from "./destroy-dom.js";
import { h, hFragment, hString } from "./h.js";
import { runWithHooks, Create, withHooks } from "./hooks.js";
import { mountDOM, type VNode } from "./mount-dom.js";
import { patchDOM } from "./patch-dom.js";
import { varState } from "./state.js";

let scheduleRender: (() => void) | null = null;

export type AppOptions<T> = {
    state: T;
    view: (state: T) => VNode;
};

// export function createApp<T>({ state, view }: AppOptions<T>) {
//     let parentEl: HTMLElement | null = null;
//     let vdom: VNode | null = null;

//     const hookedView = withHooks(view);

//     // function renderApp() {
//     //     if (vdom) destroyDOM(vdom);

//     //     // Run inside hook context
//     //     vdom = runWithHooks(hookedView as any, () => hookedView(state));

//     //     if (parentEl) {
//     //         mountDOM(vdom, parentEl);
//     //     }
//     // }

//     // Inside createApp function...

//     function renderApp() {
//         // --- 1. SNAPSHOT FOCUS STATE ---
//         const activeEl = document.activeElement as HTMLElement;
//         let isInput = false;
//         let cursorStart: number | null = null;
//         let cursorEnd: number | null = null;

//         // Check if an input is currently focused
//         if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA')) {
//             isInput = true;
//             cursorStart = (activeEl as HTMLInputElement).selectionStart;
//             cursorEnd = (activeEl as HTMLInputElement).selectionEnd;
//         }

//         // --- 2. DESTROY & RE-MOUNT (Your existing logic) ---
//         if (vdom) destroyDOM(vdom);

//         // Run inside hook context
//         vdom = runWithHooks(hookedView as any, () => hookedView(state));

//         if (parentEl) {
//             mountDOM(vdom, parentEl);
//         }

//         // --- 3. RESTORE FOCUS STATE ---
//         if (isInput && parentEl) {
//             // naive approach: find the first input (works for your example)
//             // robust approach: add an 'id' to your VNodes and find element by ID
//             const newInput = parentEl.querySelector('input, textarea') as HTMLInputElement;
            
//             if (newInput) {
//                 newInput.focus();
//                 // Restore cursor position so typing isn't interrupted
//                 if (cursorStart !== null && cursorEnd !== null) {
//                     newInput.setSelectionRange(cursorStart, cursorEnd);
//                 }
//             }
//         }
//     }

//     scheduleRender = renderApp;

//     return {
//         // mount(_parentEl: HTMLElement) {
//         //     parentEl = _parentEl;
//         //     renderApp();
//         // },
//         mount(_parentEl: HTMLElement) {
//             parentEl = _parentEl;
//             parentEl.innerHTML = "";   // <-- clear previous DOM
//             renderApp();
//         },


//         unmount() {
//             if (vdom) destroyDOM(vdom);
//         },
//     };
// }


export function createApp<T>({ state, view }: AppOptions<T>) {
    let parentEl: HTMLElement | null = null;
    let vdom: VNode | null = null; // This represents the "Old" VDOM
    let isMounted = false;         // Track if we have mounted once

    const hookedView = withHooks(view);

    function renderApp() {
        // 1. Generate the NEW Virtual DOM
        const newVdom = runWithHooks(hookedView as any, () => hookedView(state));

        // 2. If not mounted yet, Mount it.
        if (!isMounted && parentEl) {
            mountDOM(newVdom, parentEl);
            isMounted = true;
        } 
        // 3. If already mounted, PATCH it.
        else if (parentEl && vdom) {
            patchDOM(vdom, newVdom, parentEl);
        }

        // 4. Update our reference. The New becomes the Old for next time.
        vdom = newVdom;
    }

    scheduleRender = renderApp;

    return {
        mount(_parentEl: HTMLElement) {
            parentEl = _parentEl;
            parentEl.innerHTML = ""; 
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

function useOnce(fn: () => void) {
  const ran = Create(false);

  if (!ran.get()) {
    ran.set(true);
    fn();
  }
}

export { useRequest };


export {
    Create, h, mountDOM, hString, destroyDOM, hFragment, varState, varState as state, runWithHooks, withHooks, useOnce
};
export type { VNode };

export { patchDOM,  };