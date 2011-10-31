# -*- coding: utf-8 -*-

class BasicPacket:    
    data=[]

    def __init__(self):
        self.data = [0x71,0x00,0xff]

    def calc_crc(self):
        s = 0
        for w in self.data:
            s = (s + w) & 0xff
        return s
    
    def append_crc(self):
        self.data.append(self.calc_crc())

    def mk_prefix(self):
        self.data[1]=len(self.data)-1 & 0xff

    def binary(self):
        s = ""
        for w in self.data:
            s += chr(w)
        return s

    def hex(self):
        s = ""
        for w in self.data:
            s += "%0.2x " % w
        return s


class VersionPacket(BasicPacket):

    def __init__(self):
        BasicPacket.__init__(self)
        self.data.append(0x03)
        self.mk_prefix()
        self.append_crc()



class ChannelPacket(BasicPacket):

    def __init__(self):
        BasicPacket.__init__(self)
        from tv.models import Trunk
        trunks = Trunk.objects.all()
        self.data.append(0xad)
        self.data.append(0x03)
        self.data.append(trunks.count())
        for t in trunks:
            self.data.extend(t.channel_mask)
        self.mk_prefix()
        self.append_crc()        



class UserPacket(BasicPacket):

    def __init__(self,card_id):
        from lib.functions import int_to_4byte_wrapped
        BasicPacket.__init__(self)
        self.data.append(0xad)
        from tv.models import Card
        try:
            card=Card.objects.get(num=card_id)
        except Card.DoesNotExist:
            self.data.append(0x02)
        else:
            if card.active:
                self.data.append(0x01)
            else:
                self.data.append(0x02)
            c = Card.objects.count()
            self.data.extend(int_to_4byte_wrapped(c))
            self.data.extend(int_to_4byte_wrapped(card.pk))
            self.data.extend(int_to_4byte_wrapped((card.num-1)*2))
            self.data.extend(card.bin_flags)
            self.data.extend(int_to_4byte_wrapped(card.balance_int or 0))
            self.mk_prefix()
            self.append_crc()
            



class BasicQuery:

    host = '192.168.33.158'
    port = 49153
    packet= None
    request = None
    response = None
    data = {}

    def __init__(self, *args, **kwargs):
        pass

    def run(self):
        import socket
        import struct

        print "running query %s\n request: %s" % (self.__class__,self.packet.hex())

        self.response = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,struct.pack('ll',3,0))
        s.connect((self.host, self.port))
        if len(self.request) != s.send(self.request):
            return {
                "error":"cannot send to %s:%d\n$!" % (self.host, self.port),
            }
        else:
            try:
                (data,addr) = s.recvfrom(1024)                
            except socket.error, msg:                
                return {
                    "error":"socket error: %s" % msg
                }            
            except:
                return {
                    "error":"socket error: %s" % msg
                }
            self.response = data
            return self.unpack()

    def unpack(self):
        import struct

        self.data = {}
        u=struct.unpack('!3B',self.response)
        self.data.update({'len':u[0]})
        self.data.update({'result':u[1]})
        self.data.update({'checksum':u[2]})
        print "finished query %s\n data: %s" % (self.__class__,self.data)
        return self.data

    def cutzero(self,data):
        s = ''
        for c in data:
            if not c=='\x00':
                s += c
        return s



class VersionQuery(BasicQuery):

    def __init__(self, *args, **kwargs):
        self.packet=VersionPacket()
        self.request=self.packet.binary()

    def unpack(self):
        import struct

        u=struct.unpack('!B32s9B',self.response)
        self.data.update({'len':u[0]})
        self.data.update({'devname':self.cutzero(u[1])})
        self.data.update({'serial':u[2]+(u[3]<<8)+(u[4]<<16)+(u[5]<<24)})
        self.data.update({'addr':u[6]})
        self.data.update({'reserved':u[7]})
        self.data.update({'ver':"%s.%s" % (u[9],u[8])})
        self.data.update({'checksum':u[10]})
        return self.data




class ChannelQuery(BasicQuery):

    def __init__(self, *args, **kwargs):
        self.packet=ChannelPacket()
        self.request=self.packet.binary()



class UserQuery(BasicQuery):

    def __init__(self, card_id, *args, **kwargs):
        self.packet=UserPacket(card_id)
        self.request=self.packet.binary()