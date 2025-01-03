import subprocess
import sys
import threading
import os
import argparse
from termcolor import colored

def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(colored(f"Error running command '{command}': {e.stderr}", "red"))
        sys.exit(1)

def rustscan_scan(rhosts):
    """Run rustscan and retrieve open ports."""
    rustscan_command = f"rustscan -a {rhosts} --ulimit 5000 --accessible | grep 'Open' | awk -F':' '{{print $2}}' | tr -d ' ' | paste -sd,"
    return run_command(rustscan_command)

def nmap_scan(scan_type, rhosts, rports, input_file=None):
    """Run nmap scan based on the specified type (TCP/UDP)."""
    nmap_dir = "nmap"
    os.makedirs(nmap_dir, exist_ok=True)
    output_file = f"{nmap_dir}/{scan_type}_ports"

    if input_file:
        nmap_command = f"sudo nmap -sC -sV -Pn -T4 -iL {input_file} -oN {output_file}"
    else:
        if scan_type == "tcp":
            nmap_command = f"sudo nmap -sC -sV -p {rports} -Pn -T4 {rhosts} -oN {output_file}"
        elif scan_type == "udp":
            nmap_command = f"sudo nmap -sU -sC -sV -p {rports} -Pn -T4 {rhosts} -oN {output_file}"
        else:
            print(colored("Invalid scan type. Use 'tcp' or 'udp'.", "red"))
            sys.exit(1)

    print(colored(f"[+] Running nmap {scan_type.upper()} scan on {rhosts} with ports: {rports if not input_file else 'from file'}", "yellow"))
    result = run_command(nmap_command)
    print(result)

    with open(output_file, 'w') as f:
        f.write(result)

    print(colored(f"[+] Scan completed. Results saved to {output_file}", "green"))

def print_banner():
    banner = r"""
                 _   _
 _ __ ___  _   _| \ | |_ __ ___   __ _ _ __
| '_ ` _ \| | | |  \| | '_ ` _ \ / _` | '_ \
| | | | | | |_| | |\  | | | | | | (_| | |_) |
|_| |_| |_|\__, |_| \_|_| |_| |_|\__,_| .__/
           |___/                      |_|
    """
    print(colored(banner, "cyan"))

def main():
    parser = argparse.ArgumentParser(description="A fast scanning tool using RustScan and Nmap.")
    parser.add_argument("-t", "--type", choices=["tcp", "udp"], help="Type of scan: tcp or udp. Defaults to tcp.")
    parser.add_argument("-f", "--file", help="File containing list of hosts.")
    parser.add_argument("-r", "--rhosts", help="Target hosts: single IP, range (e.g., 192.168.1.1-192.168.1.10), or subnet (e.g., 192.168.1.1/24).")

    args = parser.parse_args()
    scan_type = args.type if args.type else "tcp"
    input_file = args.file
    rhosts = args.rhosts

    if not input_file and not rhosts:
        print(colored("Error: Either -f or -r must be specified.", "red"))
        sys.exit(1)

    print_banner()

    if input_file:
        print(colored("[+] Reading hosts from file...", "yellow"))
        rports = None
    else:
        print(colored("[+] Running rustscan to identify open ports...", "yellow"))
        rports = rustscan_scan(rhosts)

        if not rports:
            print(colored("[-] No open ports found. Exiting.", "red"))
            sys.exit(0)

        print(colored(f"[+] Open ports found: {rports}", "green"))

    # Run nmap scan in a separate thread
    nmap_thread = threading.Thread(target=nmap_scan, args=(scan_type, rhosts, rports, input_file))
    nmap_thread.start()
    nmap_thread.join()

if __name__ == "__main__":
    main()
