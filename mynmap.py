import subprocess
import sys
import os
import argparse
from termcolor import colored
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(colored(f"Error running command '{command}': {e.stderr}", "red"))
        sys.exit(1)

def nmap_host_discovery(rhosts, interface=None):
    nmap_command = f"nmap -sn {rhosts}"
    print(colored(f"[+] Running Nmap host discovery on {rhosts}...", "yellow"))
    result = run_command(nmap_command)

    hosts = []
    for line in result.splitlines():
        if "Nmap scan report for" in line:
            host = line.split("Nmap scan report for")[1].strip()
            host = host.split(" ")[0]
            hosts.append(host)
            print(colored(f"[+] Host discovered: {host}", "green"))

    nmap_dir = "mynmap_output"
    os.makedirs(nmap_dir, exist_ok=True)
    
    if interface:
        output_file = f"{nmap_dir}/{interface}_hosts.txt"
    else:
        output_file = f"{nmap_dir}/hosts.txt"
    
    with open(output_file, "w") as f:
        for host in hosts:
            f.write(f"{host}\n")
    
    print(colored(f"[+] Discovered hosts saved to {output_file}.", "green"))
    return hosts

def nmap_udp_scan(rhosts):
    nmap_command = f"nmap --min-rate=10000 -p- -sU -T4 -Pn {rhosts}"
    print(colored(f"[+] Running nmap UDP scan on {rhosts}...", "yellow"))
    result = run_command(nmap_command)

    open_ports = []
    for line in result.splitlines():
        if "open" in line and "/udp" in line:
            port = line.split("/")[0].strip()
            open_ports.append(port)

    if open_ports:
        print(colored(f"[+] Open UDP ports found: {', '.join(open_ports)}", "green"))
        return ",".join(open_ports)
    else:
        print(colored("[-] No open UDP ports found.", "red"))
        return None

def nmap_tcp_scan(rhosts):
    nmap_command = f"nmap --min-rate=10000 -p- -sT -T4 -Pn {rhosts}"
    print(colored(f"[+] Running nmap TCP scan on {rhosts}...", "yellow"))
    result = run_command(nmap_command)

    open_ports = []
    for line in result.splitlines():
        if "open" in line and "/tcp" in line:
            port = line.split("/")[0].strip()
            open_ports.append(port)

    if open_ports:
        print(colored(f"[+] Open TCP ports found: {', '.join(open_ports)}", "green"))
        return ",".join(open_ports)
    else:
        print(colored("[-] No open TCP ports found.", "red"))
        return None

def nmap_deep_scan(scan_type, rhosts, rports):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nmap_dir = "nmap_output"
    os.makedirs(nmap_dir, exist_ok=True)

    output_file = f"{nmap_dir}/{timestamp}_{scan_type}_ports"

    if scan_type == "udp":
        nmap_command = f"nmap --min-rate=10000 -p {rports} -sC -sV -sU -T4 -Pn {rhosts} -oA {output_file}"
    elif scan_type == "tcp":
        nmap_command = f"nmap --min-rate=10000 -p {rports} -sC -sV -sT -T4 -Pn {rhosts} -oA {output_file}"
    else:
        print(colored("Invalid scan type. Use 'tcp' or 'udp'.", "red"))
        sys.exit(1)

    print(colored(f"[+] Running nmap deep {scan_type.upper()} scan on {rhosts} with ports: {rports}", "yellow"))
    result = run_command(nmap_command)
    print(result)
    print(colored(f"[+] Scan completed. Results saved to {output_file}.", "green"))

def print_banner():
    banner = r"""
                 _   _
 _ __ ___  _   _| \ | |_ __ ___   __ _ _ __
| '_  _ \| | | |  \| | '_  _ \ / _ | '_ \
| | | | | | |_| | |\  | | | | | | (_| | |_) |
|_| |_| |_|\__, |_| \_|_| |_| |_|\__,_| .__/
           |___/                      |_|
    """
    print(colored(banner, "cyan"))

def get_ipv4_from_interface(interface):
    ip_command = f"ip addr show {interface} | grep inet | awk '{{print $2}}' | cut -d/ -f1"
    ip_address = run_command(ip_command)
    if ip_address:
        base_ip = ".".join(ip_address.split(".")[:3]) + ".0/24"
        return base_ip
    return None

def main():
    parser = argparse.ArgumentParser(description="A fast scanning tool using Nmap.")
    parser.add_argument("-t", "--type", choices=["tcp", "udp"], help="Type of scan: tcp or udp. Defaults to both.")
    parser.add_argument("-f", "--file", help="File containing list of hosts.")
    parser.add_argument("-r", "--rhosts", help="Target hosts: single IP, range (e.g., 192.168.1.1-192.168.1.10), or subnet (e.g., 192.168.1.1/24).")
    parser.add_argument("-i", "--interface", help="Network interface for host discovery (e.g., eth0, wlan0, tun0).")
    parser.add_argument("--hosts", action="store_true", help="Perform host discovery only, no port scanning.")

    args = parser.parse_args()
    scan_type = args.type if args.type else "both"
    input_file = args.file
    rhosts = args.rhosts
    interface = args.interface
    host_discovery = args.hosts

    if not input_file and not rhosts and not interface:
        print(colored("Error: Either -f, -r, or -i must be specified.", "red"))
        sys.exit(1)

    print_banner()

    if host_discovery:
        if rhosts:
            print(colored(f"[+] Discovering hosts in {rhosts}...", "yellow"))
            nmap_host_discovery(rhosts)
        elif interface:
            print(colored(f"[+] Discovering hosts on interface {interface}...", "yellow"))
            rhosts = get_ipv4_from_interface(interface)
            if not rhosts:
                print(colored(f"[-] Could not find IPv4 address for interface {interface}.", "red"))
                sys.exit(1)
            print(colored(f"[+] Using IP range {rhosts} for host discovery.", "green"))
            nmap_host_discovery(rhosts, interface=interface)
        else:
            print(colored("[-] Error: If --hosts is specified, you must provide a valid IP, range, or interface.", "red"))
            sys.exit(1)
        return

    if rhosts:
        if scan_type == "udp" or scan_type == "both":
            open_udp_ports = nmap_udp_scan(rhosts)
            if open_udp_ports:
                nmap_deep_scan("udp", rhosts, open_udp_ports)

        if scan_type == "tcp" or scan_type == "both":
            open_tcp_ports = nmap_tcp_scan(rhosts)
            if open_tcp_ports:
                nmap_deep_scan("tcp", rhosts, open_tcp_ports)

    elif input_file:
        with open(input_file, "r") as f:
            hosts = f.readlines()
        
        for host in hosts:
            host = host.strip()
            if scan_type == "udp" or scan_type == "both":
                open_udp_ports = nmap_udp_scan(host)
                if open_udp_ports:
                    nmap_deep_scan("udp", host, open_udp_ports)

            if scan_type == "tcp" or scan_type == "both":
                open_tcp_ports = nmap_tcp_scan(host)
                if open_tcp_ports:
                    nmap_deep_scan("tcp", host, open_tcp_ports)

if __name__ == "__main__":
    main()
