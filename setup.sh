#!/bin/bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install scapy
chmod +x mitm_tool.py
echo "Setup Complete! Ekhon run koren: python mitm_tool.py"
