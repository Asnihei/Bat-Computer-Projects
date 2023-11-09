
    # Projede scapy kütüphanesi kullanılacak
from scapy.all import *
import os


sym = """
 /(_M_)\\
|       |
 \/-V-\/
"""

try:
    current = os.getcwd() 
    path = os.path.join(current,"logo2.txt")  
    with open(path,"r") as file:
        art = file.read()
        print(art)


except FileNotFoundError as f:
    from art import *
    tprint("- WAYNE  -")

except (ModuleNotFoundError, NameError) as e:
    print(sym)



    # Ping atma sınıfı 
class Ping():

        # IP ve ICMP paketleri oluşturur
    def __init__(self):
        self.ip = IP()
        self.icmp = ICMP()

        self.icmpPCKT = self.ip/self.icmp


        # Belirli bir IP adresi tarar
    def sendPCKT(self, ip, iface, t=0.5):

        self.scala = ip     # hedef ip

        self.ipList = []

        
        self.icmpPCKT[IP].dst = self.scala  # hedef ip


        try:
            self.response = sr1(self.icmpPCKT, timeout=t, verbose = False, iface=iface)     # Paket gönderir

        except:
            print(sym,"İşlem başarısız. Lütfen girdiğiniz bilgileri ve bağlantınızı kontrol edin.")

        if(self.response):
            self.ipList.append(self.icmpPCKT[IP].dst)
        else:
            pass

        print(sym,"Cevap Geldi",self.ipList)



        # Belirli bir aralıkta ki IP adreslerini tarar
    def sendPCKTinRange(self, beggin, first, last, iface, t=0.5):

        self.ipList = []

            # belirtilen aralığa göre bir döngü başlatır.
        for p in range(first, last+1):

            current_ip = ""

            current_ip = beggin +"."+str(p)     # Parçalanan ip bilgisini döngüye göre yeniden birleştirir.

            self.icmpPCKT[IP].dst = current_ip      # Hedef IP


            try:    
                self.response = sr1(self.icmpPCKT, timeout=t, verbose = False, iface=iface)
                print(self.icmpPCKT[IP].dst)

            except:
                print(sym,"İşlem başarısız. Lütfen girdiğiniz bilgileri ve bağlantınızı kontrol edin.")


            if(self.response):
                self.ipList.append(self.icmpPCKT[IP].dst)
            else:
                pass

        print(sym,"Cevap Geldi",self.ipList)

    



class Broadcast:

    def __init__(self, ipdst, mac = "ff:ff:ff:ff:ff:ff", time=5):
        
        self.eth = Ether()
        self.arp = ARP()

        self.eth.dst = mac

        self.arp.pdst = ipdst

        self.bcPckt = self.eth/self.arp
        
        ans, unans = srp(self.bcPckt, timeout=time)

        print(sym)

        for snd, rcv in ans:
            print("Cevap verdi: ", rcv.src,":",rcv.psrc)




try:

    girdi = input(">> ")


    if "-p" in girdi:
        girdi = girdi.split()

        p_index = girdi.index("-p")
        packet_type = girdi[p_index+1]

        ping = Ping()

        if packet_type == "ping":

            ip_girdi = input("Taranacak IP veya IP aralığını girin: ")

            interface = input("Ağ Arayüzü: ")


            if "/" in ip_girdi:
                ip = ip_girdi.split("/")
                ip_beggin = ip[0].split(".")
                ip_end = ip[1].split(".")

                ip_core = ""

                #print(ip_beggin[3])
                #print(ip_end[3])

                ip_core = ".".join(ip_beggin[:3])   # Parçalanan IP'nin bır kısmı birleştirilir.

                print(ip_core)

                if "-t" in girdi:
                    t_index = girdi.index("-t")
                    timeOut = float(girdi[t_index+1]) 
                    print("time: ",timeOut)

                    ping.sendPCKTinRange(ip_core,int(ip_beggin[3]), int(ip_end[3]), interface, timeOut)
                
                else:
                    ping.sendPCKTinRange(ip_core,int(ip_beggin[3]), int(ip_end[3]), interface)


            elif not "/" in ip_girdi:
                if "-t" in girdi:
                    t_index = girdi.index("-t")
                    timeOut = float(girdi[t_index+1]) 
                    print("time: ",timeOut)
                
                    ping.sendPCKT(ip_girdi, interface, timeOut)

                else:
                    ping.sendPCKT(ip_girdi, interface)

            else:
                print(sym,"Lütfen uygun ip adresi veya adreslerini girin.")



        elif packet_type == "bc":

            if "-i" in girdi:
                iIndex = girdi.index("-i")
                ipIndex = girdi[iIndex+1] 


                if "-m" in girdi:
                    mindex = girdi.index("-m")
                    macindex = girdi[mindex+1]

                    br = Broadcast(ipIndex, macindex)

                else:
                    br = Broadcast(ipIndex)

                    


            else:
                print("Lütfen geçerli bir ip(-i) adresi girin")



    elif (girdi) == "help":
        print(sym,"""
            
    -p ping   =   Icmp paketleri gönderir.
    -p bc     =   Arp paketi gönderir.
    -t        =   Zaman aralığını belirler.
    -m        =   Mac adresini belirler

    Icmp örnek IP girdisi     =   185.147.1.99/185.147.1.111
    Arp örnek IP girdisi      =   185.147.1.99/24
            """)

    else:
        print(sym,"Lütfen geçerli bir paket veya komut seçin")


except Exception as e:
    print(sym,"Hatalı girdi...")
    print(e)



