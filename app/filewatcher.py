import time, threading, json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
  
class FileWatcher(FileSystemEventHandler):
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.observer = Observer()
        self.observer.schedule(self, 'recordings.db' , recursive = False)
        self.observer.start()
        self.timer = None

    def notify(self):
        new_rec = {'msg' : 'new_recording'}
        msg = json.dumps(new_rec)
        print(msg)
        self.event_queue.put_nowait(msg)

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(.2, self.notify)
            self.timer.start()
