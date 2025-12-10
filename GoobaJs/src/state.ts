import { triggerRender } from "./index.js";

const states: any[] = [];   // can hold any type
let index = 0;              // pointer for each render

export function beginComponent(): void {
    index = 0;              // reset pointer before rendering a component
}

export function varState<T>(initial: T) {
    // if value doesn't exist yet, store the initial one
    if (states[index] === undefined) {
        states[index] = initial;
    }

    const currentIndex = index;
    index++;

    function get(): T {
        return states[currentIndex] as T;
    }

    function set(newValue: T): void {
        states[currentIndex] = newValue;
        triggerRender();
    }

    return { get, set };
}
