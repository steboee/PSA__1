import binascii
import scapy.all as scapy
import dpkt


class PACKETList(list):

    def __init__(self, iterable=None):
        """Override initializer which can accept iterable"""
        super(PACKETList, self).__init__()
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, item):
        if isinstance(item, PACKET):
            super(PACKETList, self).append(item)
        else:
            raise ValueError('Ghosts allowed only')

    def insert(self, index, item):
        if isinstance(item, PACKET):
            super(PACKETList, self).insert(index, item)
        else:
            raise ValueError('Ghosts allowed only')

    def __add__(self, item):
        if isinstance(item, PACKET):
            super(PACKETList, self).__add__(item)
        else:
            raise ValueError('Ghosts allowed only')

    def __iadd__(self, item):
        if isinstance(item, PACKET):
            super(PACKETList, self).__iadd__(item)
        else:
            raise ValueError('Ghosts allowed only');




class IEEE_header:
    def __init__(self,DSAP,SSAP,type):
        self.SSAP = SSAP
        self.DSAP = DSAP
        self.type = type


class ARP_header:
    def __init__(self, Opcode, sender_MAC, sender_IP, target_MAC, target_IP):
        self.sender_MAC = sender_MAC
        self.sender_IP = sender_IP
        self.target_MAC = target_MAC
        self.target_IP = target_IP
        self.Opcode = Opcode

    def vypis(self):
        print("Sender MAC address : " + str(self.sender_MAC))
        print("Sender IP address : " + str(self.sender_IP))
        print("Target MAC address : "+ str(self.target_MAC))
        print("Target IP address : " + str(self.target_IP))




class IP_header:
    def __init__(self, protokol, source_adress, destination_adress ,length):
        self.protocol = protokol
        self.source_adress = source_adress
        self.destination_adress = destination_adress
        self.length = length

    def vypis(self):
        print("Zdrojová IP adresa : " + self.source_adress)
        print("Cieľová IP adresa : " + self.destination_adress)
        print(self.protocol.getName())

class TCP_header:
    def __init__(self, source_port, destination_port,):
        self.source_port = source_port
        self.destination_port = destination_port

    def getName(self):
        return "TCP"

    def getInfo(self):
        return self.source_port,self.destination_port

    def vypis(self):
        print("Source port : " + str(self.source_port) + "\n")
        print("Destination port : " + str(self.destination_port) + "\n")


class ICMP_header:
    def __init__(self, type):
        self.type = type

    def getName(self):
        return "ICMP"

    def getInfo(self):
        return self.type

    def vypis(self):
        print("ICMP type : " + str(self.type) + "\n")


class UDP_header:
    def __init__(self, source_port, destination_port):
        self.source_port = source_port
        self.destination_port = destination_port

    def getName(self):
        return "UDP"

    def getInfo(self):
        return self.source_port, self.destination_port

    def vypis(self):
        print("Source port : " + str(self.source_port))
        print("Destination port : " + str(self.destination_port))





mylist = PACKETList()


class PACKET:
    def __init__(self, position, length_real, length_media):
        self.position = position
        self.length_real = length_real
        self.length_media = length_media

    def set_text(self,ramec):
        self.ramec = ramec

    class Data_link_header:
        def __init__(self, destination_mac, source_mac, typ_prenosu):
            self.typ_prenosu = typ_prenosu
            self.source_mac = source_mac
            self.destination_mac = destination_mac

        def set_eth_type(self,protocol_type):
            self.eth_type = protocol_type

    class Protocol:
        pass



def length_of_packet_media(length):
    x = 0
    if (length < 60):
        x = 64
    else:
        x = length + 4
    return x


def dest_mac_adress(list_of_packet_bytes):
    destin = ""
    i = 0
    while (i != 5):
        destin = destin + str(list_of_packet_bytes[i]) + ":"
        i = i + 1
    destin = destin + str(list_of_packet_bytes[i])

    return destin


def source_mac_adress(list_of_packet_bytes):
    source = ""
    i = 6
    while (i != 11):
        source = source + str(list_of_packet_bytes[i]) + ":"
        i = i + 1
    source = source + str(list_of_packet_bytes[i])
    return source


def type_of_packet(whole_packet):
    a = whole_packet[12]
    b = whole_packet[13]
    c = a + b
    sum = int(c, 16)
    if sum >= 1536:
        type = "Ethernet II"
        # print(type)
    else:
        a = whole_packet[14]
        b = whole_packet[15]
        c = a + b
        # print(c)
        if (c == "ffff"):
            type = "IEEE 802.3 Novell RAW"
        else:
            if (c == "aaaa"):
                type = "IEEE 802.3 LLC + SNAP"
            else:
                type = "IEEE 802.3 LLC"

    return type


def file_checker(number, ID):
    number = int(number,16)
    file = open('protocols', 'r')

    for riadok in file:
        if (riadok[0] == ID):
            riadok = riadok[1:]
            a = riadok.split("=")
            if (str(number) == a[0].strip()):
                return a[1].strip()

    file.close()
    return "Unknown"



def ARP_info(packet,whole_packet):
    Opcode = whole_packet[20] + whole_packet[21]
    Opcode = int(Opcode)
    Sender_mac = ""
    Sender_ip = ""
    Target_mac = ""
    Target_ip = ""
    i = 22
    while (i != 28):
        Sender_mac = Sender_mac + str(whole_packet[i]) + ":"
        i = i + 1
    while (i != 31):
        ip = whole_packet[i]
        ip = int(ip,16)
        Sender_ip = Sender_ip + str(ip) + "."
        i = i + 1
    Sender_ip = Sender_ip + str(ip)
    i = i + 1
    while (i != 38):
        Target_mac = Target_mac + str(whole_packet[i]) + ":"
        i = i + 1
    while (i != 42):
        ip = whole_packet[i]
        ip = int(ip, 16)
        Target_ip = Target_ip + str(ip) + "."
        i = i + 1
    Target_ip = Target_ip + str(ip)
    i = i + 1
    arp = ARP_header(Opcode,Sender_mac,Sender_ip,Target_mac,Target_ip)
    return arp


def IP_info(packet,whole_packet):

    length = bin(int(whole_packet[14],16))
    length = length[2:].zfill(8)
    length = length[4:]  #z pôvodneho 1B ponechám len pravú 1/2 -> Header Length of IPv4
    length = int(length,2)*4

    protocol_number = whole_packet[23]
    protocol = file_checker(protocol_number,"-")
    source_adress = ""
    destination_adress = ""
    i = 26
    while (i != 29):
        ip = whole_packet[i]
        ip = int(ip,16)
        source_adress = source_adress + str(ip) + "."
        i = i + 1
    ip = whole_packet[i]
    ip = int(ip, 16)
    source_adress = source_adress + str(ip)
    i = i +1

    while (i != 33):
        ip = whole_packet[i]
        ip = int(ip, 16)
        destination_adress = destination_adress + str(ip) + "."
        i = i + 1
    ip = whole_packet[i]
    ip = int(ip, 16)
    destination_adress = destination_adress + str(ip)


    if (protocol == "UDP"):
        i = i + 1
        source_port = file_checker(whole_packet[i]+whole_packet[i+1],"<") + "   ->   "+ str(int(whole_packet[i] + whole_packet[i+1],16))
        destination_port = file_checker(whole_packet[i+2]+whole_packet[i+3],"<") + "   ->   "+ str(int(whole_packet[i+2] + whole_packet[i+3],16))


        UDP = UDP_header(source_port,destination_port)
        IP = IP_header(UDP, source_adress, destination_adress, length)
        return IP

    elif (protocol == "TCP"):
        i = i + 1
        source_port = file_checker(whole_packet[i] + whole_packet[i + 1], "/") + "   ->   "+ str(int(whole_packet[i] + whole_packet[i+1],16))
        destination_port = file_checker(whole_packet[i + 2] + whole_packet[i + 3], "/") + "   ->   "+ str(int(whole_packet[i+2] + whole_packet[i+3],16))
        TCP = TCP_header(source_port, destination_port)
        IP = IP_header(TCP, source_adress, destination_adress, length)
        return IP

    elif (protocol == "ICMP"):
        i = i + 1
        icmp_type = file_checker(whole_packet[0],">")
        ICMP = ICMP_header(icmp_type)
        IP = IP_header(ICMP,source_adress,destination_adress, length)
        return IP

    else:
        IP = IP_header(protocol,source_adress,destination_adress,length)
        return IP





def LoadAllPackets(pcap):
    position = 1
    for packet in pcap:
        media_length = length_of_packet_media(len(packet[1]))
        one_packet = PACKET(position, len(packet[1]), media_length)
        other = packet[1]
        pc = 0
        l = ""
        riadok = ""
        counter = 0
        whole_packet = []
        global text
        text = ""
        for x in other:
            if (counter == 0):
                riadok = "".join("{:02x}".format(x)) + " "

            elif (counter < 16):
                riadok = riadok + "".join("{:02x}".format(x)) + " "

            else:
                counter = 0
                l = str(hex(pc).lstrip("0x").rstrip("L"))
                l = l.zfill(3)
                l = l + "0"

                text = text + (l + " |   " + riadok) + "\n"
                pc = pc + 1
                riadok = "".join("{:02x}".format(x)) + " "

            counter = counter + 1
            a = "".join("{:02x}".format(x))
            whole_packet.append(a)

        text = text + (l + " |   " + riadok) + "\n"


        mylist.append(one_packet)

        src = source_mac_adress(whole_packet)
        dst = dest_mac_adress(whole_packet)

        typ_prenosu = type_of_packet(whole_packet)

        one_packet.Data_link_header = one_packet.Data_link_header(dst, src, typ_prenosu)

        if (one_packet.Data_link_header.typ_prenosu == "Ethernet II"):
            protokol_number = whole_packet[12] + whole_packet[13]
            ETHTYPE = file_checker(protokol_number, "|")  # hex číslo protokolu a špec. znak (určuje aký typ chcem hľadať)
            one_packet.Data_link_header.set_eth_type(ETHTYPE)

            if (one_packet.Data_link_header.eth_type == "ARP"):
                protocol = ARP_info(one_packet, whole_packet)
                one_packet.Protocol = protocol

            elif (one_packet.Data_link_header.eth_type == "IPv4"):
                protocol = IP_info(one_packet, whole_packet)
                one_packet.Protocol = protocol


            else:
                protocol = ""
                one_packet.Protocol = protocol

        else:
            one_packet.Data_link_header.set_eth_type("")




        one_packet.set_text(text)

        position = position + 1


def option_1(list):
    num_of_packets = list.__len__()

    print("----------------------PRINTING PACKETS-----------------------------\n\n")
    for i in range(num_of_packets):
        print(
            "--------------------------------PACKET_" + str(list[i].position) + "----------------------------------\n")

        print(list[i].ramec)
        print("Dĺžka packetu : " + str(list[i].length_real))
        print("Dĺžka packetu po médiu : " + str(list[i].length_media))
        print(list[i].Data_link_header.typ_prenosu + "\n")
        print("DESTINATION MAC ADDRESS: " + list[i].Data_link_header.destination_mac)
        print("SOURCE MAC ADDRESS: " + list[i].Data_link_header.source_mac + "\n")

        if (list[i].Data_link_header.eth_type != ""):
            print(list[i].Data_link_header.eth_type)


            if (list[i].Data_link_header.eth_type == "ARP"):
                list[i].Protocol.vypis()


            elif (list[i].Data_link_header.eth_type == "IPv4"):
                if (type(list[i].Protocol.protocol) == str):
                    print(list[i].Protocol)
                else:
                    print(list[i].Protocol.protocol.getName())
                    list[i].Protocol.protocol.vypis()





        print("\n----------------------------END OF PACKET " + str(
            list[i].position) + "-------------------------------\n\n")


def print_menu():
    print("--------------------")
    print("Analyzátor packetov")
    print("--------------------\n")
    print("Po stlačení 0 ukončí program ")
    print("Po stlačení 1 vypíše všetky komunikácie -> bod zo zadania : 1.a), 1.b), 1.c), 1.d) , 2, 3 ")
    print("Po stlačení 2 vypíše všetky komunikácie pre HTTP -> bod zo zadania : 4.a) ")
    print("Po stlačení 3 vypíše všetky komunikácie pre HTTPS -> bod zo zadania : 4.b) ")
    print("Po stlačení 4 vypíše všetky komunikácie pre TELNET -> bod zo zadania : 4.c) ")
    print("Po stlačení 5 vypíše všetky komunikácie pre SSH -> bod zo zadania : 4.d) ")
    print("Po stlačení 6 vypíše všetky komunikácie pre FTP Control -> bod zo zadania : 4.e) ")
    print("Po stlačení 7 vypíše všetky komunikácie pre FTP Data -> bod zo zadania : 4.f) ")
    print("Po stlačení 7 vypíše všetky komunikácie pre TFTP -> bod zo zadania : 4.g) ")
    print("Po stlačení 7 vypíše všetky komunikácie pre ICMP -> bod zo zadania : 4.h) ")
    print("Po stlačení 7 vypíše všetky ARP dvojice -> bod zo zadania : 4.i) ")






def main():
    with open('trace-26.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        LoadAllPackets(pcap)

        while (True):
            print_menu()
            x = input()
            if (x == "0"):
                exit()

            elif(x == "1"):
                option_1(mylist)





main()
