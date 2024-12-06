import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class LogHandler(FileSystemEventHandler):
    def __init__(self, target_directory, file_positions, positions_file):
        super().__init__()
        self.target_directory = target_directory
        self.file_positions = file_positions
        self.positions_file = positions_file

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".log"):
            return

        self.sync_file(event.src_path)

    def sync_file(self, src_path):
        with open(src_path, 'r') as file:
            current_position = self.file_positions.get(src_path, 0)
            file.seek(current_position)

            lines = file.readlines()

            new_position = file.tell()
            if current_position != new_position:
                self.file_positions[src_path] = new_position
                self.write_positions_to_file()

        if lines:
            log_filename = os.path.basename(src_path)
            target_file_path = os.path.join(self.target_directory, log_filename)

            with open(target_file_path, 'a') as target_file:
                for line in lines:
                    target_file.write(line)

            print(f"Updated logs from {src_path} to {target_file_path}")
            print("="*40)

    def write_positions_to_file(self):
        with open(self.positions_file, 'w') as f:
            json.dump(self.file_positions, f, indent=4)

def initial_sync(log_dir, target_dir, file_positions, positions_file):
    for filename in os.listdir(log_dir):
        src_path = os.path.join(log_dir, filename)
        if os.path.isfile(src_path) and filename.endswith(".log"):
            sync_file(src_path, target_dir, file_positions, positions_file)

def sync_file(src_path, target_dir, file_positions, positions_file):
    with open(src_path, 'r') as file:
        current_position = file_positions.get(src_path, 0)
        file.seek(current_position)

        lines = file.readlines()

        new_position = file.tell()
        if current_position != new_position:
            file_positions[src_path] = new_position
            write_positions_to_file(file_positions, positions_file)

    if lines:
        log_filename = os.path.basename(src_path)
        target_file_path = os.path.join(target_dir, log_filename)

        with open(target_file_path, 'a') as target_file:
            for line in lines:
                target_file.write(line)

        print(f"Initial sync of logs from {src_path} to {target_file_path}")
        print("="*40)

def write_positions_to_file(file_positions, positions_file):
    with open(positions_file, 'w') as f:
        json.dump(file_positions, f, indent=4)

def load_positions_from_file(positions_file):
    if os.path.exists(positions_file):
        with open(positions_file, 'r') as f:
            return json.load(f)
    return {}

def monitor_logs(log_dir, target_dir, positions_file):
    file_positions = load_positions_from_file(positions_file)
    initial_sync(log_dir, target_dir, file_positions, positions_file)

    print(f"initial_sync finished")

    event_handler = LogHandler(target_dir, file_positions, positions_file)
    observer = Observer()
    observer.schedule(event_handler, log_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    log_directory = "D:/logs/sources/"  # Replace with actual log file location
    target_directory = "D:/logs/target/"  # Ensure this path exists and is writable
    positions_file = "file_positions.json"  # File to save the file positions

    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    monitor_logs(log_directory, target_directory, positions_file)
