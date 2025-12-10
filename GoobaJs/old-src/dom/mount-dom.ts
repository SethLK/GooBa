import { DOM_TYPES } from "../h.js";

export interface VNode {
  type: string;
  tag?: string;
  props?: Record<string, any>;
  children?: VNode[];
  value?: string;
  el?: HTMLElement | Text | null;
  listeners?: Record<string, EventListener>;
}


export function mountDOM(vdom: VNode, parentEl: HTMLElement) {
  switch (vdom.type) {
    case DOM_TYPES.TEXT: {
      createTextNode(vdom, parentEl);
      break;
    }
    case DOM_TYPES.ELEMENT: {
      createElementNode(vdom, parentEl);
      break;
    }
    case DOM_TYPES.FRAGMENT: {
      createFragmentNodes(vdom, parentEl);
      break;
    }
    default: {
      throw new Error(`Can't mount DOM of type: ${vdom.type}`);
    }
  }
}

function createTextNode(vdom: { value?: string, el?: any }, parentEl: { append: (node: Text) => void }) {
  const { value } = vdom
  const textNode = document.createTextNode(value ?? '')
  vdom.el = textNode
  parentEl.append(textNode)
}



function createElementNode(vdom: VNode, parentEl: HTMLElement) {
  const { tag, props = {}, children = [] } = vdom
  if (!tag) throw new Error("VNode is missing tag")
  const element = document.createElement(tag)
  addProps(element, props, vdom)
  vdom.el = element
  children.forEach(child => mountDOM(child, element))
  parentEl.appendChild(element)
}

function addProps(
  el: HTMLElement,
  props: Record<string, any>,
  vdom: VNode
) {
  const { on: events = {}, ...attrs } = props
  vdom.listeners = addEventListeners(events, el)
  setAttributes(el, attrs)
}


function createFragmentNodes(vdom: VNode, parentEl: HTMLElement) {
  vdom.el = parentEl
  vdom.children?.forEach(child => mountDOM(child, parentEl))
}


export function addEventListener(eventName: any, handler: any, el: { addEventListener: (arg0: any, arg1: any) => void; }) {
  el.addEventListener(eventName, handler);
  return handler;
}

type EventMap = { [eventName: string]: (event: Event) => void }

export function addEventListeners(
  listeners: EventMap = {},
  el: HTMLElement
): Record<string, EventListener> {
  const addedListeners: Record<string, EventListener> = {}

  Object.entries(listeners).forEach(([eventName, handler]) => {
    const listener: EventListener = (event) => handler(event)
    el.addEventListener(eventName, listener)
    addedListeners[eventName] = listener
  })

  // return listeners
  return addedListeners

}

interface StyleMap {
  [prop: string]: string | number
}

interface Attrs {
  class?: string | string[]
  style?: StyleMap
  [key: string]: any
}

export function setAttributes(el: HTMLElement, attrs: Attrs): void {
  const { class: className, style, ...otherAttrs } = attrs

  if (className) {
    setClass(el, className)
  }

  if (style) {
    Object.entries(style).forEach(([prop, value]) => {
      setStyle(el, prop as keyof CSSStyleDeclaration, value)
    })
  }

  for (const [name, value] of Object.entries(otherAttrs)) {
    setAttribute(el, name, value)
  }
}

function setClass(el: HTMLElement, className: string | string[]): void {
  el.className = '' // clear existing classes

  if (typeof className === 'string') {
    el.className = className
  } else if (Array.isArray(className)) {
    el.classList.add(...className)
  }
}

export function setStyle(
  el: HTMLElement,
  name: keyof CSSStyleDeclaration,
  value: string | number
): void {
  // @ts-ignore: allow dynamic assignment to CSSStyleDeclaration
  el.style[name] = value as any
}

export function removeStyle(
  el: HTMLElement,
  name: keyof CSSStyleDeclaration
): void {
  // @ts-ignore: allow dynamic assignment to CSSStyleDeclaration
  el.style[name] = ''
}

export function setAttribute(
  el: HTMLElement,
  name: string,
  value: string | number | null | undefined
): void {
  if (value == null) {
    removeAttribute(el, name)
  } else if (name.startsWith('data-')) {
    el.setAttribute(name, String(value))
  } else {
    // @ts-ignore: dynamic property assignment
    el[name] = value
  }
}

export function removeAttribute(el: HTMLElement, name: string): void {
  // @ts-ignore: dynamic property assignment
  el[name] = null
  el.removeAttribute(name)
}
