# mynmap

`mynmap` is a Python-based tool that integrates RustScan and Nmap for efficient and fast network scanning. It supports TCP and UDP scans, allows scanning single IPs, IP ranges, subnets, or reading hosts from a file. Results are displayed on the console and saved for further analysis.

---

## Features

- **TCP and UDP Scans**: Choose between TCP and UDP scans with Nmap.
- **RustScan Integration**: Utilizes RustScan to quickly identify open ports.
- **Flexible Target Specification**: Scan single IPs, IP ranges, subnets, or use a file for input.
- **Multithreaded Scanning**: Ensures faster scans.
- **Save and Display Results**: Outputs scan results both on the terminal and saves them to a file.
- **Interactive Banner**: Includes a colorful ASCII art banner for a user-friendly interface.

---

## Requirements

- Python 3.6+
- RustScan installed and accessible via the command line.
- Nmap installed and accessible via the command line.
- `termcolor` Python library for colored output. Install it using:
  ```bash
  pip install termcolor
  ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cyb4x/myNmap.git
   ```
2. Navigate to the project directory:
   ```bash
   cd myNmap
   ```
3. Make the script executable:
   ```bash
   chmod +x mynmap.py
   ```

---

## Usage

Run `mynmap` with `sudo` to ensure proper permissions for Nmap.

### Basic Syntax

```bash
sudo python3 mynmap.py -t <scan_type> [-f <file>] [-r <targets>]
```

### Examples

#### Default TCP Scan (if `-t` is not specified)
```bash
sudo python3 mynmap.py -r 192.168.1.2
```

#### TCP Scan on a Subnet
```bash
sudo python3 mynmap.py -t tcp -r 192.168.1.0/24
```

#### UDP Scan on a Range of IPs
```bash
sudo python3 mynmap.py -t udp -r 192.168.1.1-192.168.1.10
```

#### Scan Hosts from a File
```bash
sudo python3 mynmap.py -t tcp -f targets.txt
```

---

## Output

- Results are displayed on the terminal during the scan.
- A detailed scan report is saved in the `nmap/` directory with filenames corresponding to the scan type, e.g., `nmap/tcp_ports` or `nmap/udp_ports`.

---

## Help Menu

Access the help menu for detailed options:
```bash
python3 mynmap.py -h
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your fork and create a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
