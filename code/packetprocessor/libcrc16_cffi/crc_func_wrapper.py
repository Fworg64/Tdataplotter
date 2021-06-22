from libcrc16_cffi import ffi, lib

def crc16_func_w(bytes, length):
  bb = ffi.new("char[]", bytes[0:length])
  crc_check = lib.crc_16(bb, length)
  return crc_check