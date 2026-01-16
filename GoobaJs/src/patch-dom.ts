// patch-dom.ts
import { destroyDOM } from "./destroy-dom.js";
import { mountDOM, setAttribute, removeAttribute, type VNode, addEventListeners } from "./mount-dom.js"; // Reuse your existing tools
import { DOM_TYPES } from "./h.js";

export function patchDOM(oldVNode: VNode, newVNode: VNode, parentEl: HTMLElement) {
  // 1. If the old node didn't exist, just mount the new one (shouldn't happen in patch, but safe)
  if (!oldVNode) {
    mountDOM(newVNode, parentEl);
    return;
  }

  if (!newVNode) {
    destroyDOM(oldVNode);
    return;
  }
  if (oldVNode.tag !== newVNode.tag || oldVNode.type !== newVNode.type) {
    mountDOM(newVNode, parentEl);
    destroyDOM(oldVNode); // Remove old form DOM
    return;
  }

  const el = (newVNode.el = oldVNode.el!);

  if (newVNode.type === DOM_TYPES.TEXT) {
    if (oldVNode.value !== newVNode.value) {
      el.nodeValue = newVNode.value!;
    }
    return;
  }

  patchProps(el as HTMLElement, oldVNode.props || {}, newVNode.props || {}, oldVNode);
  
  patchChildren(el as HTMLElement, oldVNode.children || [], newVNode.children || []);
}

function patchProps(el: HTMLElement, oldProps: any, newProps: any, oldVNode: VNode) {
  
  for (const key in newProps) {
    const oldVal = oldProps[key];
    const newVal = newProps[key];

    if (oldVal !== newVal) {
      if (key === 'on') {
      } else {
         setAttribute(el, key, newVal);
      }
    }
  }

  for (const key in oldProps) {
    if (!(key in newProps)) {
       removeAttribute(el, key);
    }
  }
}

function patchChildren(el: HTMLElement, oldChildren: VNode[], newChildren: VNode[]) {
  const oldLength = oldChildren.length;
  const newLength = newChildren.length;
  
  const length = Math.max(oldLength, newLength);

  for (let i = 0; i < length; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];

    if (oldChild && newChild) {
      patchDOM(oldChild, newChild, el);
    } else if (!oldChild && newChild) {
      mountDOM(newChild, el);
    } else if (oldChild && !newChild) {
      destroyDOM(oldChild);
    }
  }
}