let currentEffect: (() => void) | null = null;

// Type for a reactive signal
export interface Signal<T> {
  get(): T;
  set(newValue: T): void;
}

export function signal<T>(value: T): Signal<T> {
  const subscribers = new Set<() => void>();

  const get = (): T => {
    if (currentEffect) subscribers.add(currentEffect);
    return value;
  };

  const set = (newValue: T): void => {
    value = newValue;
    subscribers.forEach((fn) => fn());
  };

  return { get, set };
}

// Optional: helper for registering effects
export function effect(fn: () => void): void {
  currentEffect = fn;
  fn();
  currentEffect = null;
}
