# For setting up the file system observer
from watchdog.observers import Observer
# For handling file system events
from watchdog.events import FileSystemEventHandler
import time  # For time-related functions
import os  # Provides functions for interacting with the operating system


def get_non_conflicting_name(dst):
    """Generates a new file name if a file with the same name already exists."""
    counter = 1
    base_name, extension = os.path.splitext(dst)
    while os.path.exists(dst):
        dst = f"{base_name} ({counter}){extension}"
        counter += 1
    return dst


class Handler(FileSystemEventHandler):
    def process(self, event):
        print(f"Event detected: {event}")
        for file in os.listdir(watched_folder):
            if file.startswith('~$') or file.endswith('.tmp'):
                continue  # Skip temporary files

            src = os.path.join(watched_folder, file)
            dst = os.path.join(destination_folder, file)

            if os.path.isdir(src):
                continue  # Skip directories

            try:
                if os.path.exists(dst):
                    dst = get_non_conflicting_name(dst)
                print(f"Moving {src} to {dst}")
                os.rename(src, dst)
            except FileNotFoundError:
                print(f"File not found: {src}")
            except Exception as e:
                print(f"Error moving file: {e}")

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":
    watched_folder = input("Enter the path of the folder to watch: ")
    destination_folder = input("Enter the path of the destination folder: ")

    # Check if the folders exist
    if not os.path.exists(watched_folder):
        print(f"The watched folder '{watched_folder}' does not exist.")
        exit()
    if not os.path.exists(destination_folder):
        print(f"The destination folder '{destination_folder}' does not exist.")
        exit()

    # Set up the file observer and handler
    handler = Handler()
    observer = Observer()
    observer.schedule(event_handler=handler,
                      path=watched_folder, recursive=True)
    observer.start()

    # Run the observer
    print(f"Monitoring {watched_folder} for changes. To stop, press Ctrl+C.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("File monitoring stopped.")
