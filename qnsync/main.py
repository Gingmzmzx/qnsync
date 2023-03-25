import qiniu.config, time, os, json, threading, sys, click
from qiniu import Auth, put_file, etag, BucketManager
from watchdog.observers import Observer
from watchdog.events import *
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

access_key = None
secret_key = None
bucket_name = None
monitor_path = "."
base_dir = "/"

def loadConfig(config_path="config.json"):
    with open(config_path, 'r') as f:
        data = json.loads(f.read())
        
        # for k, v in data.items():
        #     exec(f"{k} = v")
        
        global access_key, secret_key, bucket_name, monitor_path, base_dir
        access_key = data.get("access_key")
        secret_key = data.get("secret_key")
        bucket_name = data.get("bucket_name")
        monitor_path = data.get("monitor_path", monitor_path)
        base_dir = data.get("base_dir", base_dir)

class FileHandler:
    q = None
    bucket = None
    
    def __init__(self):
        self.q = Auth(access_key, secret_key)
        self.bucket = BucketManager(self.q)
    
    def upload(self, i, flag=True):
        key = self._(i)
        token = self.q.upload_token(bucket_name, key, 3600)
        ret, info = put_file(token, key, i, version='v2')
        if flag:
            assert ret['key'] == key, info
            assert ret['hash'] == etag(i), info
            print("Modified File:", i, "Status:", info.status_code)
        return ret, info
    
    def delete(self, i, flag=True):
        ret, info = self.bucket.delete(bucket_name, self._(i))
        if flag:
            assert ret == {}, info
            print("Delete File:", i, "Status:", info.status_code)
        return ret, info
    
    def move(self, i, flag=True):
        key, key2 = i
        ret, info = self.bucket.move(bucket_name, self._(key), bucket_name, self._(key2))
        if flag:
            assert ret == {}, info
            print("Move File:", i, "Status:", info.status_code)
        return ret, info

    def _(self, path):
        return f"{base_dir}{path.replace(monitor_path, '')}"
    
    def on_files_created(self, path):
        for i in path:
            self.upload(i)

    def on_files_deleted(self, path):
        for i in path:
            self.delete(i)

    def on_files_modified(self, path):
        for i in path:
            self.delete(i, flag=False)
            self.upload(i)
    
    def on_files_moved(self, path):
        for i in path:
            self.move(i)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, aim_path):
        FileSystemEventHandler.__init__(self)
        self.aim_path = aim_path
        self.timer = None
        self.snapshot = DirectorySnapshot(self.aim_path)
        self.handler = FileHandler()
    
    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        
        self.timer = threading.Timer(0.2, self.checkSnapshot)
        self.timer.start()
    
    def checkSnapshot(self):
        snapshot = DirectorySnapshot(self.aim_path)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None
        
        for i in dir(self.handler):
            if i[0:3] != "on_" or not callable(getattr(self.handler, i)):
                continue    
            ob = getattr(diff, i.replace("on_", ""))
            if ob:
                getattr(self.handler, i)(ob)

class DirMonitor(object):
    """文件夹监视类"""
    
    def __init__(self, aim_path):
        """构造函数"""
        self.aim_path= aim_path
        self.observer = Observer()
    
    def start(self):
        """启动"""
        event_handler = FileEventHandler(self.aim_path)
        self.observer.schedule(event_handler, self.aim_path, True)
        self.observer.start()
    
    def stop(self):
        """停止"""
        self.observer.stop()

@click.command()
@click.option("--path", default="config.json", help="Path to the config file")
def cli(path):
    loadConfig(path)

    monitor = DirMonitor(monitor_path) 
    monitor.start() 
    try: 
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt: 
        monitor.stop()

if __name__ == "__main__":
    cli()