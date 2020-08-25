import netfilterqueue
import time

def process_packet(packet):
    print("\rCutting off target internet connection...\\", end = '')
    time.sleep(0.13)
    print("\rCutting off target internet connection...|", end = '')
    time.sleep(0.13)
    print("\rCutting off target internet connection.../", end = '')
    time.sleep(0.13)
    print("\rCutting off target internet connection...-", end = '')
    time.sleep(0.13)
    packet.drop()

queue = netfilterqueue.NetfilterQueue()
print("Net cutter initialised")
queue.bind(0,process_packet)
queue.run()