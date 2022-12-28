import subprocess
import argparse
import re

class Raptor():
    def __init__(self, ip, scan_web):
        self.ip = ip
        self.scan_web = scan_web 

        self.banner()
        self.scan()

    def out(self, s):
        print(s)
        with open("results", "a") as f:
            f.write(s)
    
    def banner(self):
        banner = ""
        banner += '                      __\n'
        banner += '____________  _______/  |_  ___________\n'
        banner += '\_  __ \__  \ \____ \   __\/  _ \_  __ \\\n'
        banner += ' |  | \// __ \|  |_> >  | (  <_> )  | \/\n'
        banner += ' |__|  (____  /   __/|__|  \____/|__|\n'
        banner += '            \/|__|\n'
        banner += "\n---- Raptor Autorecon ----\n"
        banner += f"\nIP: {self.ip}\n"
        self.out(banner)
    
    def scan(self):
        self.nmap_tcp_100()
        self.nmap_tcp_all()
        ports, http_ports = self.parse_open_ports()
        self.nmap_tcp_int(ports)
        self.nmap_udp_100()

        if scan_web:
            self.web_enum(http_ports)

    def web_enum(self, http_ports):
        for port in http_ports:
            self.gobuster(port)
            self.nikto(port)
            self.whatweb(port)
            
    def gobuster(self, port):
        self.out(f"\n---- Gobuster (Port {port}) ----\n")
        cmd = f"gobuster dir -u {self.ip}:{port} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o gobuster_{port}.log -x php,html,txt -f -n -k"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)

    def nikto(self, port):
        self.out(f"\n---- Nikto (Port {port}) ----\n")
        cmd = f"nikto -host={self.ip} -output=nikto_{port}.txt"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)

    def whatweb(self, port):
        self.out(f"\n---- WhatWeb (Port {port}) ----\n")
        cmd = f"whatweb {self.ip} -v --log-verbose whatweb_{port}.txt"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)
    
    def parse_open_ports(self, nmap_file="nmap_tcp_all.txt"):
        http_ports = []
        ports = []
        with open(nmap_file, "r") as f:
            lines = f.readlines()
        for line in lines:
            if "/tcp" in line:
                port = re.findall(r'\d+', line)[0]
                if "http" in line:
                    http_ports.append(port)
                ports.append(port)
        return ports, http_ports
    
    def nmap_tcp_100(self):
        self.out("\n---- Nmap TCP (Top 100) ----\n")
        cmd = f"nmap {ip} --top-ports 100 -Pn --open -oN nmap_tcp_100.txt"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)

    def nmap_tcp_all(self):
        self.out("\n---- Nmap TCP (All) ----\n")
        cmd = f"nmap {ip} -p- -sT -T4 -Pn --open -oN nmap_tcp_all.txt"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)
    
    def nmap_tcp_int(self, ports):
        self.out("\n---- Nmap TCP (Aggressive) ----\n")
        ports_fmt = ",".join(ports)
        cmd = f"nmap {self.ip} -p {ports_fmt} -A -T4 -Pn --open -oN nmap_tcp_int.txt"
        return
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)
    
    def nmap_udp_100(self):
        self.out("\n---- Nmap UDP (Top 100) ----\n")
        cmd = f"nmap {self.ip} -sU -T4 -Pn --top-ports 100 --open -oN nmap_udp_100.txt"
        out = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        self.out(out.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raptor Autorecon")
    parser.add_argument("ip", help="Target IP")
    parser.add_argument("-w", "--web", help="Perform web scanning (Y/n)")
    args = vars(parser.parse_args())

    ip = args["ip"]
    web = args["web"]
    scan_web = True
    if web.lower() == "n":
        scan_web = False

    raptor = Raptor(ip, scan_web)

