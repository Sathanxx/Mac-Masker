#!/usr/bin/env python3

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Network interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more details.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address. Use --help for details.")

    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ifconfig", interface]).decode()
    except subprocess.CalledProcessError:
        return None
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
    if mac_search:
        return mac_search.group(0)
    else:
        return None

if __name__ == "__main__":
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    print(f"Current MAC: {current_mac}")
    change_mac(options.interface, options.new_mac)
    updated_mac = get_current_mac(options.interface)
    if updated_mac == options.new_mac:
        print(f"[+] MAC address successfully changed to {updated_mac}")
    else:
        print("[-] MAC address change failed.")
