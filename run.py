import time
import subprocess
import os
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from server import PORT

class ServerManager:
    def __init__(self):
        self.process = None

    def start_server(self):
        self.stop_server()  # always stop before start
        self.process = subprocess.Popen(['python', 'server.py'])

    def stop_server(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def restart_server(self):
        print(f"\n♻️ Restarting server on port {PORT} ...")
        subprocess.run(['python', './Gooba/Templix/Templix.py', '.'])
        subprocess.run(['python', 'main.py'])
        self.start_server()


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, server_manager):
        self.server_manager = server_manager

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File changed: {event.src_path}")
            self.server_manager.restart_server()


if __name__ == "__main__":
    server_manager = ServerManager()
    server_manager.start_server()

    observer = Observer()
    event_handler = ChangeHandler(server_manager)
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    print("👀 Watching for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        server_manager.stop_server()
    observer.join()
