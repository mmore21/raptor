# raptor

Automatic enumeration tool for penetration testing.

## Description

Raptor automatically enumerates a system by performing common scans. This includes:

- [gobuster](https://github.com/OJ/gobuster)
- [nikto](https://github.com/sullo/nikto)
- [nmap](https://nmap.org/)
- [whatweb](https://github.com/urbanadventurer/WhatWeb)

## Usage

No dependencies are required. To run raptor, simply clone the repository and run the Python 3 script.

```sh
git clone https://github.com/mmore21/raptor.git
cd raptor/
python3 raptor/raptor.py -h
usage: raptor.py [-h] [-w WEB] ip

Raptor Autorecon

positional arguments:
  ip                 Target IP

optional arguments:
  -h, --help         show this help message and exit
  -w WEB, --web WEB  Perform web scanning (Y/n)
```

## License

raptor is available under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/).

