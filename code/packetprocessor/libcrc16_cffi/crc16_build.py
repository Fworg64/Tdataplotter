from cffi import FFI

import os
lib_dir = os.path.dirname(os.path.realpath(__file__)) 

ffibuilder = FFI()

ffibuilder.cdef("""
    uint16_t crc_16( const unsigned char *input_str, size_t num_bytes );
""")

ffibuilder.set_source("libcrc16_cffi",
"""
    #include "include/checksum.h"
""",
    libraries=['crc16'],
    library_dirs=[lib_dir] )

if __name__ == "__main__":
  ffibuilder.compile(verbose=True) 
  print("Don't forget to install the shared library!")
  print("Use: sudo cp ./libcrc16.so /usr/local/lib/libcrc16.so")
  print("Then: sudo ldconfig")
