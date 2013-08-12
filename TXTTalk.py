import socket
import struct

class DNSQuery:
  def __init__(Self, Data):
    Self.Data=Data
    Self.Domain=''

    tipo = (ord(Data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(Data[ini])
      while lon != 0:
        Self.Domain+=Data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(Data[ini])

  def ReplyTXT(Self,ReplyString):
    Packet=''
    if Self.Domain:
      ReplyLength = len(ReplyString)
      Packet+=Self.Data[:2] + "\x81\x80"
      Packet+=Self.Data[4:6] + Self.Data[4:6] + '\x00\x00\x00\x00' #Questions and Answers Counts
      Packet+=Self.Data[12:] #Original Domain Name Question
      Packet+='\xc0\x0c' #Pointer to domain name
      Packet+='\x00\x10\x00\x01\x00\x00\x00\x3c' #Reply type and TTL
      Packet+=struct.pack(">h",ReplyLength + 1) #Data Legnth     
      Packet+=struct.pack(">b", ReplyLength) #TXT Length
      Packet+=ReplyString #TXT
    return Packet

if __name__ == '__main__':
  print 'TXTTalk Server Active'
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))
  LogFile = open('TXTTalk_Log.txt','a')
  HelloString='Message Received'
  try:
    while 1:
      Data, addr = udps.recvfrom(1024)
      Query=DNSQuery(Data)
      udps.sendto(Query.ReplyTXT(HelloString), addr)
      print 'Request: %s Replied With: %s' % (Query.Domain,HelloString)
      LogFile.write('Request:  ' + Query.Domain + ' Replied With ' + HelloString)
  except KeyboardInterrupt:
    print 'Exiting...'
    udps.close()
    f.close()
