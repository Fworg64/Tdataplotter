import serial
from pathlib import Path
import time
from threading import Thread
import pdb

class SerialRecorder():
  state_list = ["Waiting for connection... ", "Recording", "Timed out"]
  def __init__(self, device_str_in):
    self.bytelist = []
    self.state_index = 0
    self.device_str = device_str_in
    self.stop_req = False

    self.baudrate = 115200
    self.timeout = 2.0
    self.sub_interval = 1000
    self.ser_init = False
    self.ser = serial.Serial(self.device_str, baudrate=self.baudrate, timeout = self.timeout)
    self.ser_init = True
    self.rec_thread = None

  def __del__(self):
    if self.ser_init:
      self.ser.close()

  def stop(self):
    self.stop_req = True
    self.rec_thread.join() # Block until thread reads flag
    self.rec_thread = None
    self.save_bytelist_to_file()

  def start_recording_session(self):
    if self.rec_thread is None:
      self.rec_thread = Thread(target = self.record_session)
      self.rec_thread.start()

  def record_session(self):
    while not self.stop_req:
      s = self.ser.read(self.sub_interval)
      self.bytelist.extend(s)
      if len(s) < self.sub_interval: # timeout happened
        if self.state_index == 0: # Waiting for connection
          continue
        else: # Connection timed out
          self.state_index = 2
          break
      else:
        self.state_index = 1 # Recording

  def save_bytelist_to_file(self):
    record_byte_array = bytearray(self.bytelist)
    Path("out").mkdir(parents=True, exist_ok=True)
    outfilename = "out/" + "cap_rec_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    with open(outfilename, "wb") as outfile:
      outfile.write(record_byte_array)
    print("saved file to {0}".format(outfilename))
