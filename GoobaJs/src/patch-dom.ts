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

  // 2. If the new node doesn't exist? We should remove the old one.
  // (Usually handled by parent patch logic, but good safeguard)
  if (!newVNode) {
    destroyDOM(oldVNode);
    return;
  }

  // 3. DIFFERENT TAGS? -> REPLACE
  // If tags are different (e.g. div vs span), assume tree is totally different.
  // Destroy old, mount new.
  if (oldVNode.tag !== newVNode.tag || oldVNode.type !== newVNode.type) {
    mountDOM(newVNode, parentEl);
    destroyDOM(oldVNode); // Remove old form DOM
    return;
  }

  // 4. SAME TAGS? -> UPDATE
  // We keep the existing DOM element!
  // Transfer the actual DOM element reference from old to new VNode
  const el = (newVNode.el = oldVNode.el!);

  // A. TEXT NODES
  if (newVNode.type === DOM_TYPES.TEXT) {
    if (oldVNode.value !== newVNode.value) {
      el.nodeValue = newVNode.value!;
    }
    return; // Text nodes don't have props or children
  }

  // B. ELEMENT NODES
  // Patch Props
  patchProps(el as HTMLElement, oldVNode.props || {}, newVNode.props || {}, oldVNode);
  
  // Patch Children
  patchChildren(el as HTMLElement, oldVNode.children || [], newVNode.children || []);
}

function patchProps(el: HTMLElement, oldProps: any, newProps: any, oldVNode: VNode) {
  // 1. Add/Update new props
  for (const key in newProps) {
    const oldVal = oldProps[key];
    const newVal = newProps[key];

    if (oldVal !== newVal) {
      // Special handler for Event Listeners
      if (key === 'on') {
          // This is tricky. Simplified: remove old listeners, add new ones.
          // Ideally, your VNode stores a reference to the listener function to remove it specifically.
          // For now, let's just re-run addEventListeners logic (which might duplicate if not careful).
          // **Better approach for this lesson:** // We won't implement full event patching logic here to keep it simple, 
          // but usually, you remove the old listener and add the new one.
          
          // Let's assume your 'on' object keys are stable (click, input).
          // You might need to expose a removeEventListener helper from mount-dom.
      } else {
         setAttribute(el, key, newVal);
      }
    }
  }

  // 2. Remove old props that are missing in new props
  for (const key in oldProps) {
    if (!(key in newProps)) {
       removeAttribute(el, key);
    }
  }
}

function patchChildren(el: HTMLElement, oldChildren: VNode[], newChildren: VNode[]) {
  const oldLength = oldChildren.length;
  const newLength = newChildren.length;
  
  // Iterate over the longer length to cover all bases
  const length = Math.max(oldLength, newLength);

  for (let i = 0; i < length; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];

    if (oldChild && newChild) {
      // Both exist? Patch them.
      patchDOM(oldChild, newChild, el);
    } else if (!oldChild && newChild) {
      // New child exists, old doesn't? It's an insertion.
      mountDOM(newChild, el);
    } else if (oldChild && !newChild) {
      // Old exists, new doesn't? It's a removal.
      destroyDOM(oldChild);
    }
  }
}