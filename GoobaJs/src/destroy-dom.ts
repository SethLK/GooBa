import { removeEventListeners } from "./events.js";
import { DOM_TYPES } from "./h.js";
import type { VNode } from "./mount-dom.js";

export function destroyDOM(vdom: VNode): void {
  const { type } = vdom;

  switch (type) {
    case DOM_TYPES.TEXT:
      removeTextNode(vdom);
      break;

    case DOM_TYPES.ELEMENT:
      removeElementNode(vdom);
      break;

    case DOM_TYPES.FRAGMENT:
      removeFragmentNodes(vdom);
      break;

    default:
      throw new Error(`Can't destroy DOM of type: ${type}`);
  }

  delete vdom.el;
}

function removeTextNode(vdom: VNode): void {
  const el = vdom.el;
  if (el instanceof Text) {
    el.remove();
  }
}

function removeElementNode(vdom: VNode): void {
  const { el, children = [], listeners } = vdom;

  if (el instanceof HTMLElement) {
    el.remove();
  }

  // Remove children from DOM tree
  children.forEach(child => destroyDOM(child));

  // Remove event listeners
  if (listeners) {
    removeEventListeners(listeners, el as HTMLElement);
    delete vdom.listeners;
  }
}


function removeFragmentNodes(vdom: VNode): void {
  const { children = [] } = vdom;
  children.forEach(child => destroyDOM(child));
}
