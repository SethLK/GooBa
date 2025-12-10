export class Dispatcher<TCommands extends string = string> {
  // Map of commandName → array of handlers
  #subs: Map<TCommands, Array<(payload?: any) => void>> = new Map()
   #afterHandlers: Array<() => void> = []

  subscribe(
    commandName: TCommands,
    handler: (payload?: any) => void
  ): () => void {
    if (!this.#subs.has(commandName)) {
      this.#subs.set(commandName, [])
    }

    const handlers = this.#subs.get(commandName)!
    
    if (handlers.includes(handler)) {
      return () => {}
    }

    handlers.push(handler)

    return () => {
      const idx = handlers.indexOf(handler)
      if (idx !== -1) handlers.splice(idx, 1)
    }
  }

  dispatch(commandName: TCommands, payload?: any): void {
    if (this.#subs.has(commandName)) {
      this.#subs.get(commandName)!.forEach((handler) => handler(payload))
    } else {
      console.warn(`No handlers for command: ${commandName}`)
    }

    this.#afterHandlers.forEach((handler) => handler())
  }

  after(handler: () => void): () => void {
    this.#afterHandlers.push(handler)

    // Return unsubscribe function
    return () => {
      const idx = this.#afterHandlers.indexOf(handler)
      if (idx !== -1) {
        this.#afterHandlers.splice(idx, 1)
      }
    }
  }
}
