#!/bin/bash

echo "[*] Updating System..."
pkg update && pkg upgrade -y

echo "[*] Installing Python and Dependencies..."
pkg install python git tsu -y

echo "[*] Installing Python Libraries..."
pip install scapy

chmod +x mitm_tool.py
echo "[+] Setup Complete! Use 'sudo python mitm_tool.py' to run."
