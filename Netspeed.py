#!/usr/bin/env python3
import psutil
import time
import argparse
import os
from tabulate import tabulate

# Meta
__version__ = "2.4"
__author__ = "MalwareHunterz"
__toolname__ = "NetSpeed"
__description__ = "Advanced Network Speed Monitoring Tool with Detailed Interface Stats"

# Color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"

# Banner
BANNER = f"""{BOLD}{MAGENTA}
.----------------------------------------------.
|  _   _      _   _____                     _  |
| | \ | |    | | /  ___|                   | | |
| |  \| | ___| |_\ `--. _ __   ___  ___  __| | |
| | . ` |/ _ \ __|`--. \ '_ \ / _ \/ _ \/ _` | |
| | |\  |  __/ |_/\__/ / |_) |  __/  __/ (_| | |
| \_| \_/\___|\__\____/| .__/ \___|\___|\__,_| |
|                      | |                     |
|                      |_|                     |
'----------------------------------------------'
{RESET}"""

# Help text
HELP_TEXT = f"""
{BANNER}
{BOLD}{CYAN}NetSpeed {__version__} by {__author__}{RESET}
{__description__}

{BOLD}USAGE:{RESET}
  netspeed [options]

{BOLD}OPTIONS:{RESET}
  {BOLD}-i, --interface{RESET} [interface_name]   Monitor specified interface (e.g., eth0, wlan0).
  {BOLD}-all{RESET}                              Monitor all interfaces separately.
  {BOLD}-c, --combined{RESET}                    Monitor combined speeds of all interfaces.
  {BOLD}-r, --refresh{RESET} [seconds]           Set refresh rate (default: 0.1 seconds, minimum possible rate).
  {BOLD}-b, --bits{RESET}                        Show speed in bits per second (default: bytes per second).
  {BOLD}-p, --packets{RESET}                     Display packet counts (sent/received) per interface.
  {BOLD}-e, --errors{RESET}                      Show error count per interface.
  {BOLD}-d, --dropped{RESET}                     Show dropped packet count per interface.
  {BOLD}-f, --full{RESET}                        Display the most detailed view (all info combined).
  {BOLD}-h, --help{RESET}                        Show this help menu.
"""

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", "--interface", type=str, help="Specify the interface (e.g. eth0)")
    parser.add_argument("-all", action="store_true", help="Monitor all interfaces individually")
    parser.add_argument("-c", "--combined", action="store_true", help="Combine up/download speed of all interfaces")
    parser.add_argument("-r", "--refresh", type=float, default=1, help="Set the refresh rate (in seconds, default 0.1)")
    parser.add_argument("-b", "--bits", action="store_true", help="Display speed in bits per second")
    parser.add_argument("-p", "--packets", action="store_true", help="Show packet counts")
    parser.add_argument("-e", "--errors", action="store_true", help="Show error count per interface")
    parser.add_argument("-d", "--dropped", action="store_true", help="Show dropped packet count per interface")
    parser.add_argument("-f", "--full", action="store_true", help="Display the most detailed view available")
    parser.add_argument("-h", "--help", action="store_true", help="Display help menu")
    return parser.parse_args()

def format_speed(value, use_bits):
    """Formats speed to human-readable form."""
    if use_bits:
        units = ["bps", "Kbps", "Mbps", "Gbps"]
        factor = 8
    else:
        units = ["Bps", "KBps", "MBps", "GBps"]
        factor = 1

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

def get_interface_stats(interfaces, use_bits):
    """Fetches and returns network statistics for the specified interfaces."""
    stats = {}
    for iface in psutil.net_if_addrs():
        if interfaces is None or iface == interfaces:
            stats[iface] = psutil.net_if_stats()[iface]
            net_io = psutil.net_io_counters(pernic=True)[iface]
            sent_bytes = net_io.bytes_sent
            recv_bytes = net_io.bytes_recv
            pkts_sent = net_io.packets_sent
            pkts_recv = net_io.packets_recv
            errin = net_io.errin
            errout = net_io.errout
            dropin = net_io.dropin
            dropout = net_io.dropout
            stats[iface] = (sent_bytes, recv_bytes, pkts_sent, pkts_recv, errin, errout, dropin, dropout)
    return stats

def display_speed(interfaces, refresh_rate, use_bits, show_packets, show_errors, show_dropped, combined=False):
    previous_stats = get_interface_stats(interfaces, use_bits)
    
    try:
        while True:
            os.system('clear')
            print(BANNER)
            print(f"{CYAN}{BOLD}NetSpeed - Live Network Monitoring{RESET}")
            print(f"{BOLD}{GREEN}INTERFACE MONITORING:{RESET}")

            current_stats = get_interface_stats(interfaces, use_bits)
            table_data = []

            total_sent = total_recv = 0

            for iface, (prev_sent, prev_recv, prev_pkts_sent, prev_pkts_recv, prev_errin, prev_errout, prev_dropin, prev_dropout) in previous_stats.items():
                curr_sent, curr_recv, curr_pkts_sent, curr_pkts_recv, curr_errin, curr_errout, curr_dropin, curr_dropout = current_stats.get(iface, (0, 0, 0, 0, 0, 0, 0, 0))
                
                sent_speed = (curr_sent - prev_sent) / refresh_rate
                recv_speed = (curr_recv - prev_recv) / refresh_rate
                total_sent += sent_speed
                total_recv += recv_speed

                row = [f"{MAGENTA}{iface}{RESET}", format_speed(sent_speed, use_bits), format_speed(recv_speed, use_bits)]
                if show_packets:
                    row.extend([f"{curr_pkts_sent} / {curr_pkts_recv}"])
                if show_errors:
                    row.extend([f"{curr_errin} / {curr_errout}"])
                if show_dropped:
                    row.extend([f"{curr_dropin} / {curr_dropout}"])

                table_data.append(row)

            if combined:
                row = [f"{MAGENTA}All{RESET}", format_speed(total_sent, use_bits), format_speed(total_recv, use_bits)]
                table_data.append(row)

            headers = [f"{CYAN}Interface{RESET}", f"{GREEN}Upload Speed{RESET}", f"{RED}Download Speed{RESET}"]
            if show_packets:
                headers.append(f"{GREEN}Packets Sent/Received{RESET}")
            if show_errors:
                headers.append(f"{RED}Errors In/Out{RESET}")
            if show_dropped:
                headers.append(f"{GREEN}Dropped In/Out{RESET}")

            table = tabulate(table_data, headers=headers, tablefmt="fancy_grid", maxcolwidths=[20, 20, 20])
            print(table)
            print(f"{CYAN}{BOLD}Press CTRL+C to close{RESET}")

            previous_stats = current_stats
            time.sleep(refresh_rate)

    except KeyboardInterrupt:
        print(f"\n{BLUE}Closing NetSpeed... Goodbye!{RESET}")
        time.sleep(1)

def main():
    args = parse_args()
    
    if args.help:
        print(HELP_TEXT)
        return
    
    if args.interface and args.all:
        print(f"{RED}Error:{RESET} You cannot specify an interface and use -all at the same time.")
        return
    
    interfaces = None if args.all else args.interface
    refresh_rate = args.refresh
    use_bits = args.bits
    combined = args.combined and not args.all
    show_packets = args.packets
    show_errors = args.errors
    show_dropped = args.dropped

    if args.full:
        show_packets = True
        show_errors = True
        show_dropped = True

    display_speed(interfaces, refresh_rate, use_bits, show_packets, show_errors, show_dropped, combined)

if __name__ == "__main__":
    main()
