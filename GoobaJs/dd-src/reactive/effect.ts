let currentEffect: (() => void) | null = null;

export function effect(fn: () => void): void {
  currentEffect = fn;
  fn();
  currentEffect = null;
}
