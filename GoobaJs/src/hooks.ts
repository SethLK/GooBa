import { triggerRender } from "./index.js";

type Hook = any;

interface HookComponent {
    hooks: Hook[];
    hookIndex: number;
    (props?: any): any;
}

/**
 * Wrap a view function so it can use hooks.
 */
export function withHooks<T extends (...args: any[]) => any>(fn: T): T {
    const wrapped: HookComponent = function (props?: any) {
        wrapped.hookIndex = 0;
        return fn(props);
    } as any;

    wrapped.hooks = [];
    wrapped.hookIndex = 0;

    return wrapped as unknown as T;
}

let current: HookComponent | null = null;

/**
 * Run a component with hook context.
 */
export function runWithHooks<T>(component: HookComponent, fn: () => T): T {
    current = component;
    const out = fn();
    current = null;
    return out;
}

/**
 * React-like useState 
 */
export function Create<T>(initial: T): { 
    get: () => T;
    set: (value: T | ((prev: T) => T)) => void;
} {
    if (!current) {
        throw new Error("Create() must be called inside a hooked component");
    }

    const hooks = current.hooks;
    const idx = current.hookIndex++;

    if (hooks[idx] === undefined) {
        hooks[idx] = initial;
    }

    const get = () => hooks[idx] as T;

    const set = (value: T | ((prev: T) => T)) => {
        if (typeof value === "function") {
            hooks[idx] = (value as (prev: T) => T)(hooks[idx]);
        } else {
            hooks[idx] = value;
        }

        triggerRender();
    };


    return { get, set };
}
