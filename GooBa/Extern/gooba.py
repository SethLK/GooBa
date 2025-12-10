goooba = """

// src/events.ts
function removeEventListeners(listeners = {}, el) {
  Object.entries(listeners).forEach(([eventName, handler]) => {
    el.removeEventListener(eventName, handler);
  });
}

// src/h.ts
function withoutNulls(arr) {
  return arr.filter((item) => item != null);
}
function mapTextNodes(children) {
  return children.map(
    (child) => typeof child === "string" ? hString(child) : child
  );
}
function hString(str) {
  return { type: DOM_TYPES.TEXT, value: str };
}
var DOM_TYPES = {
  TEXT: "text",
  ELEMENT: "element",
  FRAGMENT: "fragment"
};
function h(tag, props = {}, children = []) {
  return {
    tag,
    props,
    children: mapTextNodes(withoutNulls(children)),
    type: DOM_TYPES.ELEMENT
  };
}
function hFragment(vNodes) {
  return {
    type: DOM_TYPES.FRAGMENT,
    children: mapTextNodes(withoutNulls(vNodes))
  };
}

// src/destroy-dom.ts
function destroyDOM(vdom) {
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
function removeTextNode(vdom) {
  const el = vdom.el;
  if (el instanceof Text) {
    el.remove();
  }
}
function removeElementNode(vdom) {
  const { el, children = [], listeners } = vdom;
  if (el instanceof HTMLElement) {
    el.remove();
  }
  children.forEach((child) => destroyDOM(child));
  if (listeners) {
    removeEventListeners(listeners, el);
    delete vdom.listeners;
  }
}
function removeFragmentNodes(vdom) {
  const { children = [] } = vdom;
  children.forEach((child) => destroyDOM(child));
}

// src/hooks.ts
function withHooks(fn) {
  const wrapped = function(props) {
    wrapped.hookIndex = 0;
    return fn(props);
  };
  wrapped.hooks = [];
  wrapped.hookIndex = 0;
  return wrapped;
}
var current = null;
function runWithHooks(component, fn) {
  current = component;
  const out = fn();
  current = null;
  return out;
}
function Create(initial) {
  if (!current) {
    throw new Error("Create() must be called inside a hooked component");
  }
  const hooks = current.hooks;
  const idx = current.hookIndex++;
  if (hooks[idx] === void 0) {
    hooks[idx] = initial;
  }
  const get = () => hooks[idx];
  const set = (value) => {
    if (typeof value === "function") {
      hooks[idx] = value(hooks[idx]);
    } else {
      hooks[idx] = value;
    }
    triggerRender();
  };
  return { get, set };
}

// src/mount-dom.ts
function mountDOM(vdom, parentEl) {
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
function createTextNode(vdom, parentEl) {
  const { value } = vdom;
  const textNode = document.createTextNode(value ?? "");
  vdom.el = textNode;
  parentEl.append(textNode);
}
function createElementNode(vdom, parentEl) {
  const { tag, props = {}, children = [] } = vdom;
  if (!tag) throw new Error("VNode is missing tag");
  const element = document.createElement(tag);
  addProps(element, props, vdom);
  vdom.el = element;
  children.forEach((child) => mountDOM(child, element));
  parentEl.appendChild(element);
}
function addProps(el, props, vdom) {
  const { on: events = {}, ...attrs } = props;
  vdom.listeners = addEventListeners(events, el);
  setAttributes(el, attrs);
}
function createFragmentNodes(vdom, parentEl) {
  vdom.el = parentEl;
  vdom.children?.forEach((child) => mountDOM(child, parentEl));
}
function addEventListeners(listeners = {}, el) {
  const addedListeners = {};
  Object.entries(listeners).forEach(([eventName, handler]) => {
    const listener = (event) => handler(event);
    el.addEventListener(eventName, listener);
    addedListeners[eventName] = listener;
  });
  return addedListeners;
}
function setAttributes(el, attrs) {
  const { class: className, style, ...otherAttrs } = attrs;
  if (className) {
    setClass(el, className);
  }
  if (style) {
    Object.entries(style).forEach(([prop, value]) => {
      setStyle(el, prop, value);
    });
  }
  for (const [name, value] of Object.entries(otherAttrs)) {
    setAttribute(el, name, value);
  }
}
function setClass(el, className) {
  el.className = "";
  if (typeof className === "string") {
    el.className = className;
  } else if (Array.isArray(className)) {
    el.classList.add(...className);
  }
}
function setStyle(el, name, value) {
  el.style[name] = value;
}
function setAttribute(el, name, value) {
  if (value == null) {
    removeAttribute(el, name);
  } else if (name.startsWith("data-")) {
    el.setAttribute(name, String(value));
  } else {
    el[name] = value;
  }
}
function removeAttribute(el, name) {
  el[name] = null;
  el.removeAttribute(name);
}

// src/state.ts
var states = [];
var index = 0;
function varState(initial) {
  if (states[index] === void 0) {
    states[index] = initial;
  }
  const currentIndex = index;
  index++;
  function get() {
    return states[currentIndex];
  }
  function set(newValue) {
    states[currentIndex] = newValue;
    triggerRender();
  }
  return { get, set };
}

// src/index.ts
var scheduleRender = null;
function createApp({ state, view }) {
  let parentEl = null;
  let vdom = null;
  const hookedView = withHooks(view);
  function renderApp() {
    if (vdom) destroyDOM(vdom);
    vdom = runWithHooks(hookedView, () => hookedView(state));
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
    mount(_parentEl) {
      parentEl = _parentEl;
      parentEl.innerHTML = "";
      renderApp();
    },
    unmount() {
      if (vdom) destroyDOM(vdom);
    }
  };
}
function triggerRender() {
  if (scheduleRender) scheduleRender();
}
export {
  Create,
  createApp,
  destroyDOM,
  h,
  hFragment,
  hString,
  mountDOM,
  runWithHooks,
  varState as state,
  triggerRender,
  varState,
  withHooks
};
//# sourceMappingURL=gooba.js.map


"""