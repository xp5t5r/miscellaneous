import sys, os

TS_BYTES = "\x47\x1F\xFF"
REC_BYTES = "\x54\x46\x72" # "TFr"
ZERO_BYTES = "\x00\x00\x00"

def main():
  if len(sys.argv) == 1:
    print "rec2ts.py - Convert Topfield .rec to .ts (and back again)\n"
    print "Usage: python rec2ts.py <filename>\n"
    sys.exit()

  filename = sys.argv[1]
  file = open(filename, "r+b")
  header = file.read(3760)
  chunks = headerToChunks(header, 188)

  if isRecFile(chunks):
    header = toTsHeader(chunks)
    newname = filename[:-3] + "ts"
  elif isTsFile(chunks):
    header = toRecHeader(chunks)
    newname = filename[:-2] + "rec"
  else:
    sys.exit("Unrecognized file format '" + filename + "'")

  file.seek(0)
  file.write(header)
  file.close()

  os.rename(filename, newname)
  print "Successfully converted '" + filename + "' to '" + newname + "'"

def headerToChunks(string, length):
  return [string[i:i+length] for i in range(0, len(string), length)]

def isRecFile(chunks):
  return chunks[0][:3] == REC_BYTES

def isTsFile(chunks):
  return chunks[19][:6] == TS_BYTES + REC_BYTES

def toTsHeader(chunks):
  topfieldBytes = chunks[0][:3] + chunks[1][:3]
  chunks = [replaceBytes(chunk, TS_BYTES) for chunk in chunks]
  chunks[19] = replaceBytes(chunks[19], topfieldBytes, 3)
  return "".join(chunks)

def toRecHeader(chunks):
  topfieldBytes = chunks[19][3:9]
  chunks = [replaceBytes(chunk, ZERO_BYTES) for chunk in chunks]
  chunks[19] = replaceBytes(chunks[19], ZERO_BYTES + ZERO_BYTES, 3)
  chunks[0] = replaceBytes(chunks[0], topfieldBytes[:3])
  chunks[1] = replaceBytes(chunks[1], topfieldBytes[3:6])
  return "".join(chunks)

def replaceBytes(chunk, bytes, start=0):
  return chunk.replace(chunk[start:len(bytes)+start], bytes, 1)  

if __name__ == '__main__':
  main()
