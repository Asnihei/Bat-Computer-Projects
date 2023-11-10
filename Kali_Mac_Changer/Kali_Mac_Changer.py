
import random

import re

import subprocess

import os


sym = """
 /(_M_)\\
|       |
 \/-V-\/
"""

try:
    from art import *

    current = os.getcwd() 
    path = os.path.join(current,"logo2.txt")  
    with open(path,"r") as file:
        art = file.read()
        print(art)


except FileNotFoundError as f:
    tprint("- WAYNE  -")

except (ModuleNotFoundError, NameError) as e:
    print(sym)





charList = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

def createRandom(i):
    try:
        newMAC = ""


        for m in range(6):
            newMAC += random.choice(charList)
            newMAC += random.choice(charList)
            
            if m != 5:
                newMAC += ":"


        MAC = subprocess.check_output(f"ifconfig {i}", shell=True).decode()

        oldMAC = re.search("ether (.+)", MAC).group()


        subprocess.check_output(f"ifconfig {i} down", shell=True)
        subprocess.check_output(f"ifconfig {i} hw ether "+newMAC, shell=True)
        subprocess.check_output(f"ifconfig {i} up", shell=True)

        MAC = subprocess.check_output(f"ifconfig {i}", shell=True).decode()

        newMAC = re.search("ether (.+)", MAC).group()

        print(f"Eski MAC: {oldMAC}\nYeni MAC: {newMAC}")
        
    
    except Exception as e:
        print("Bir hatayla karşılaştık.",e)
        subprocess.check_output(f"ifconfig {i} up", shell=True)


def setMAC(s, i):

    try:
        oldMAC = subprocess.check_output(f"ifconfig {i}", shell=True).decode()

        subprocess.check_output(f"ifconfig {i} down", shell=True)
        subprocess.check_output(f"ifconfig {i} hw ether "+s, shell=True)
        subprocess.check_output(f"ifconfig {i} up", shell=True)

        newMAC = subprocess.check_output(f"ifconfig {i}", shell=True).decode()

    
    except Exception as e:
        print("Bir hatayla karşılaştık.",e)
        subprocess.check_output(f"ifconfig {i} up", shell=True)




try:
    while True:
        
        girdi = input("> ")

        if "exit" in girdi:
            break


        elif "help" in girdi:
            print(""" 
    -i = Ağ arayüzü
    -r = Rastgele mac
    -s = Kendi macini yaz
            """)



        elif "-r" in girdi:
            if "-i" in girdi:
                girdis = girdi.split()
                iIndex = girdis.index("-i")
                interface = girdis[iIndex+1]

                createRandom(interface)

            else:
                print("Bir ağ arayüzü belirlemelisin")

        elif "-s" in girdi:

            girdis = girdi.split()

            sindex = girdis.index("-s")
            macindex = girdis[sindex+1]

            if "-i" in girdi:
                girdis = girdi.split()
                iIndex = girdis.index("-i")
                interface = girdis[iIndex+1]

                setMAC(macindex, interface)

            else:
                print("Bir ağ arayüzü belirlemelisin")




        else:
            print("Girdi Hatası")


except subprocess.CalledProcessError as s:
    print("Root yetkisi gerekli")

