
export function removeEventListeners(
  listeners: Record<string, EventListener> = {},
  el: HTMLElement
): void {
  Object.entries(listeners).forEach(([eventName, handler]) => {
    el.removeEventListener(eventName, handler);
  });
}