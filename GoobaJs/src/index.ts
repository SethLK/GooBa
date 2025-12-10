
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

export {
    Create, h, mountDOM, hString, destroyDOM, hFragment, varState, varState as state, runWithHooks, withHooks
};
export type { VNode };