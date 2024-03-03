from loader import LocalUploader
from watchdog.observers import Observer

if __name__ == '__main__':
    uploader = LocalUploader()
    observer = Observer()
    observer.schedule(uploader, uploader.history_directory, recursive=True)
    observer.schedule(uploader, uploader.origin_directory, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
