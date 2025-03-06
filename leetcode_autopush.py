import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo

class LeetCodeWatcher(FileSystemEventHandler):
    def __init__(self, repo):
        self.repo = repo

    def on_modified(self, event):
        if not event.is_directory:
            self.commit_changes(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.commit_changes(event.src_path)

    def commit_changes(self, file_path):
        self.repo.git.add(file_path)
        commit_message = f"Auto commit: {os.path.basename(file_path)}"
        self.repo.git.commit(m=commit_message)
        self.repo.git.push()
        print(f"Pushed changes for {file_path}")

def start_watching(path):
    repo = Repo(path)
    event_handler = LeetCodeWatcher(repo)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Starting to watch {path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    local_repo_path = "G:\PycharmProject"
    start_watching(local_repo_path)
