from libcrc16_cffi import ffi, lib
import pdb

print("Loaded shared object file with function {0}".format(lib.crc_16))

bb = ffi.new("char[]", "DOG-TOOTHv03".encode("UTF-8"))
crc_val = lib.crc_16(bb, 12)
print("Got CRC of {0}".format(crc_val))