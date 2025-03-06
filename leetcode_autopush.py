import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
from git.exc import GitCommandError

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        # 排除不需要提交的文件和目录
        if (file_path.startswith('.idea/') or
                file_path.endswith('~') or
                file_path == '.git' or
                file_path == 'leetcode_autopush.py'):
            logging.warning(f"Skipping unwanted file: {file_path}")
            return

        # 检查文件是否存在
        if not os.path.isfile(file_path):
            logging.warning(f"File does not exist: {file_path}")
            return

        try:
            # 添加所有修改（包括关联文件）
            self.repo.git.add('.')

            commit_message = f"Auto commit: {os.path.basename(file_path)}"
            self.repo.git.commit(m=commit_message)
            self.repo.git.push()
            logging.info(f"Pushed changes for {file_path}")
        except GitCommandError as e:
            logging.error(f"Failed to commit or push changes: {e}")


def start_watching(path):
    try:
        repo = Repo(path)
        event_handler = LeetCodeWatcher(repo)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        logging.info(f"Starting to watch {path}...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping watcher...")
        observer.stop()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        observer.join()


if __name__ == "__main__":
    local_repo_path = r"G:/PycharmProject"
    start_watching(local_repo_path)