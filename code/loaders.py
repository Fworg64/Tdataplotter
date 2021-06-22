
import packetprocessor.packet_processor as ppr
import csv

def load_cap_file(input_file):
  packer = ppr.packetProcessor()
  packet_list = []
  with open(input_file, "rb") as infile:
    # give each byte to state packitizer
    # collect packets when given
    cur_byte = infile.read(1)
    while (cur_byte): # reading eol gives "False"
      state, ret = packer.give_byte(cur_byte)
      if ret is not None:
        packet_list.append(ret)
      cur_byte = infile.read(1)
  return packet_list

def load_frame_file(input_file):
  packet_list = []
  with open(input_file, "r") as infile:
    reader = csv.reader(infile, delimiter="	")
    for idx, row in enumerate(reader):
      if idx < 5:
        continue
      else:
        packet = {"kN": float(row[0]), "mm": float(row[1]), "Sec": float(row[2])}
        packet_list.append(packet)
  return packet_list
