export function withoutNulls(arr: any[]) {
    return arr.filter((item) => item != null);
}

function mapTextNodes(children: any[]) {
    return children.map((child: any) =>
        typeof child === 'string' ? hString(child) : child
    );
}

export function hString(str: string) {
    return { type: DOM_TYPES.TEXT, value: str };
}

export const DOM_TYPES = {
    TEXT: 'text',
    ELEMENT: 'element',
    FRAGMENT: 'fragment',
};

export function h(tag: any, props = {}, children = []) {
    return {
        tag,
        props,
        children: mapTextNodes(withoutNulls(children)),
        type: DOM_TYPES.ELEMENT,
    };
}

export function hFragment(vNodes: any[]) {
    return {
        type: DOM_TYPES.FRAGMENT,
        children: mapTextNodes(withoutNulls(vNodes)),
    };
}