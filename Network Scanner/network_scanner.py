import scapy.all as scapy
import threading
import optparse
import time
import os
import signal

def scan(ip):
    global listed
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 0.1, verbose = False)[0]
    clients_list = []
    for element in answered_list:
        if element[1].psrc not in listed:
            client_dict = {"ip" : element[1].psrc, "mac": element[1].hwsrc}
            clients_list.append(client_dict)
            listed.append(element[1].psrc)
    print_result( clients_list)

def print_result(result):
    for client in result:
        print("\r                                                 ",end='')
        print("\r"+client["ip"]+"\t\t"+client["mac"])

def increment(i):
    global num
    for j in range(0,256):
        scan((num[0]+"."+num[1]+"."+str(i)+"."+str(j)))

def get_input():
    global ip
    parser = optparse.OptionParser()

    parser.add_option("-i", "--ip_address", dest = "address", help = "Attackers ip address")

    (options, arguments) = parser.parse_args()
    print("\nEntered ip address: "+str(options.address))
    ip = options.address

def input_error():
    print("\n[-]Values not entered. Try 'sudo python3 <program_name>.py --help' for more help and information.\n")

def loader():
    global n
    try:
        print("\rChecking for ip addresses within the network...\\", end="")
        time.sleep(0.13)
        print("\rChecking for ip addresses within the network...|", end="")
        time.sleep(0.13)
        print("\rChecking for ip addresses within the network.../", end="")
        time.sleep(0.13)
        print("\rChecking for ip addresses within the network...-", end="")
        time.sleep(0.13)
        loader()
    except:
        parent_pid = os.getppid()
        if parent_pid:
            os.kill(parent_pid, signal.SIGSTOP)
        exit()




ip = ""
num=[]
get_input()
print("\nIP\t\t\tMAC Address\n--------------------------------------------")
n=0
listed=[]
parent_pid=0

try:
    if ip==None:
        input_error()
    else:
        num = ip.split(".")
        ip = num[0]+"."+num[1]+"."+num[2]+"."
        n = os.fork()

        if n == 0:  # child process
            loader()

        if n > 0:  # parent process
            parent_pid = os.getpid()
            for iterator in range(0,255):
                scan(ip+str(iterator))
        print("\r--------------------------------------------          ")
        print("\n[+]Scanning of ip address immediate to the given addresses complete. ")
        print("\n[+]Now scanning for more distant ip addresses and any previously unresponsive ips... Please continue waiting only if any other addresses are suspected.")
        print("[+]This may take a while...\n")
        print("\r--------------------------------------------          ")
        for i in range(0,256):
            for j in range(0,255):
                if (num[0]+"."+num[1]+"."+str(i)+"."+str(j)) not in listed:
                    scan(num[0]+"."+num[1]+"."+str(i)+"."+str(j))

        os.kill(n,signal.SIGSTOP)
except:
    if n:
        os.kill(n, signal.SIGSTOP)
    print("\r[-] Detected Ctrl+C... Exitting program... Please wait...")

    exit()
