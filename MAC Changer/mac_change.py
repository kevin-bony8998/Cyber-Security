import subprocess
import optparse

def get_input():
    global interface, mac
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest = "inter", help = "Interface whose MAC address is to be changed.")
    parser.add_option("-m", "--mac", dest = "mc", help = "New MAC address.")

    (options, arguments) = parser.parse_args()
    print("Option entered: "+str(options.inter))
    interface = options.inter
    mac = options.mc

def input_error():
    print("\n[-]Values not entered. Try 'sudo python3 <program_name>.py --help' for more help and information.\n")


interface = ""
mac = ""
get_input()
if interface==None or mac == None:
    input_error()
else:
    subprocess.call("ifconfig "+interface+" down", shell= True)
    subprocess.call("ifconfig "+interface+" hw ether "+mac, shell= True)
    subprocess.call("ifconfig "+interface+" up", shell=True)

#00:d8:61:2f:c4:44