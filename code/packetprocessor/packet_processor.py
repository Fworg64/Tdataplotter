from threading import Thread
from time import sleep
import pdb

from packetprocessor.libcrc16_cffi.libcrc16_cffi import ffi, lib

class PacketProcessorManager:
  def __init__(self):
    self.stop_req = False
    self.num_processed = 0
    self.ppro = packetProcessor()
    self.packet_list = []
    self.valid_packet_list = []
    self.pro_thread = None
    self.all_processed = False
  
  def start_watch_list(self, the_list):
    if self.pro_thread is None:
      self.pro_thread = Thread(target = self.watch_list_at, args = (the_list,))
      self.pro_thread.start()

  def watch_list_at(self, the_list):
    while not self.stop_req:
      if len(the_list) > self.num_processed:
        self.all_processed = False
        state, ret = self.ppro.give_byte(the_list[self.num_processed].to_bytes(1, 'big'))
        if ret is not None:
          self.packet_list.append(ret)
          if ret["crc_valid"]:
            self.valid_packet_list.append(ret)
        self.num_processed += 1
      else:
        self.all_processed = True

  def stop_when_done(self):
    while not self.all_processed:
      sleep(0.5)
    self.stop_req = True
    self.pro_thread.join()
    self.pro_thread = None


class packetProcessor:
  pp_state_list = ["FINDING_HEADER_1", "FINDING_HEADER_2", "LOAD_SEQ_HI", "LOAD_SEQ_LO",
                 "LOAD_CHAN_A_1", "LOAD_CHAN_A_2", "LOAD_CHAN_B_1", "LOAD_CHAN_B_2",
                 "LOAD_CHAN_C_1", "LOAD_CHAN_C_2", "LOAD_CHAN_D_1", "LOAD_CHAN_D_2", 
                 "LOAD_CRC_HI", "LOAD_CRC_LO"]
  def __init__(self):
    self.state_index = 0
    self.state = self.pp_state_list[self.state_index]
    self.current_packet = {'header': 0, 'seq': 0, 'chan_a': 0, 'chan_b': 0, 
                           'chan_c': 0, 'chan_d': 0, 'crc': 0, 'crc_valid': 0} 
    self.current_bytes = []
    self.prev_0 = 0

  def give_byte(self, byte):
    try:
      assert isinstance(byte, bytes)
    except AssertionError:
      print("input was {0} with class {1}".format(byte, type(byte)))
    ret_val = None

#    if self.prev_0 >= 2:
#      self.state_index = 2
#      self.prev_0 = 0   
#      self.current_bytes = [b'\x00', b'x\00']
      
    if self.state_index <= 1:
      if byte == b'\x00': # good
        self.current_bytes.append(byte)
        self.state_index += 1
      else: # bad, start over
        self.current_bytes = []
        self.state_index = 0
    elif self.state_index >= 2 and self.state_index <= 12:
      self.current_bytes.append(byte)      
      self.state_index += 1
    else: # state_index = 13
      self.current_bytes.append(byte) 
      success = self.fill_packet_with_bytes()
      # reset state
      self.current_bytes = []
      self.state_index = 0
      if success:
        ret_val = self.current_packet.copy()

#    if byte == b'\x00':
#      self.prev_0 += 1
#    else:
#      self.prev_0 = 0
    
    self.state = self.pp_state_list[self.state_index]
    return self.state, ret_val 

  def fill_packet_with_bytes(self):
    if len(self.current_bytes) == len(self.pp_state_list):
      self.current_packet['header'] = (ord(self.current_bytes[0]) << 8) + ord(self.current_bytes[1])
      self.current_packet['seq']    = (ord(self.current_bytes[3]) << 8) + ord(self.current_bytes[2])
      self.current_packet['chan_a'] = (ord(self.current_bytes[4]) << 8) + ord(self.current_bytes[5])
      self.current_packet['chan_b'] = (ord(self.current_bytes[6]) << 8) + ord(self.current_bytes[7])
      self.current_packet['chan_c'] = (ord(self.current_bytes[8]) << 8) + ord(self.current_bytes[9])
      self.current_packet['chan_d'] = (ord(self.current_bytes[10])<< 8) + ord(self.current_bytes[11])
      self.current_packet['crc']    = (ord(self.current_bytes[13])<< 8) + ord(self.current_bytes[12])
      # check crc value
      bb = ffi.new("char[]", self.current_bytes[0:12])
      crc_check = lib.crc_16(bb, 12)
      self.current_packet['crc_valid'] = crc_check == self.current_packet['crc']
      return True
    else:
      return False

    

    