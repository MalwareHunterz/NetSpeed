# NetSpeed
![netspeed](https://github.com/user-attachments/assets/d16f4bd0-9974-4ddb-8eb7-d6392430e8ed)

## Overview
NetSpeed is an advanced network speed monitoring tool that provides real-time statistics on network interfaces. It displays upload and download speeds, packet counts, and error counts, making it an essential utility for network analysis.

## Features
- Monitor specified network interfaces.
- Detailed statistics for upload/download speeds in bytes or bits per second.
- Packet count display for sent and received packets.
- Error and dropped packet statistics.
- Configurable refresh rate for real-time monitoring.
- Combines data for all interfaces for a comprehensive overview.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/NetSpeed.git
   cd NetSpeed

    Install the required packages:

    bash

    pip install -r requirements.txt

## Usage

Run the script with options as needed:

```bash

python NetSpeed.py [options]

Options

    -i, --interface [interface_name] Monitor specified interface (e.g., eth0, wlan0).
    -all Monitor all interfaces separately.
    -c, --combined Monitor combined speeds of all interfaces.
    -r, --refresh [seconds] Set refresh rate (default: 0.1 seconds, minimum possible rate).
    -b, --bits Show speed in bits per second (default: bytes per second).
    -p, --packets Display packet counts (sent/received) per interface.
    -e, --errors Show error count per interface.
    -d, --dropped Show dropped packet count per interface.
    -f, --full Display the most detailed view (all info combined).
    -h, --help Show this help menu.
```
## Example

To monitor the eth0 interface:

```bash

python NetSpeed.py -i eth0 -r 1
```
To view all interfaces combined:

```bash

python NetSpeed.py -c -r 1
``` 
## Author

MalwareHunterz

## License

This project is licensed under the MIT License - see the LICENSE file for details.
