from threading import Thread
from time import sleep

class FileStreamer:
  def __init__(self, file_path, rate_bps=115200, repeat=True):
    self.file = open(file_path, 'br')
    self.bytes_per_second = int(rate_bps / 9 / 10) # 8 data and 1 stop bit (stop bit not in file), 10 times/sec
    self.repeat = repeat
    self.stop_req = False
    self.byte_list = []
    self.stream_thread = Thread(target = self.stream_file)
    self.stream_thread.start()
   
  def stream_file(self):
    while not self.stop_req:
      some_chars = self.file.read(self.bytes_per_second)
      self.byte_list.extend(some_chars)
      if len(some_chars) < self.bytes_per_second:
        if self.repeat:
          self.file.seek(0)
        else:
          self.stop_req = True
      sleep(0.1)
    
  def __del__(self):
    self.file.close()