#!/usr/bin/env python3
import os
import argparse
import subprocess

def read_meminfo():
    with open('/proc/meminfo', 'r') as file:
        return {line.split(':')[0]: int(line.split()[1]) for line in file.readlines()}

def calculate_memory(meminfo):
    return meminfo['MemTotal'] - meminfo['MemAvailable'], meminfo['MemTotal']

def get_pids(program):
    try:
        return list(map(int, subprocess.check_output(['pidof', program]).strip().split()))
    except subprocess.CalledProcessError:
        return []

def process_memory(pid):
    try:
        with open(f'/proc/{pid}/smaps', 'r') as file:
            return sum(int(line.split()[1]) for line in file if line.startswith('Rss:'))
    except FileNotFoundError:
        return 0

def display_program_memory(program):
    pids = get_pids(program)
    total = 0
    for pid in pids:
        rss = process_memory(pid)
        total += rss
        print(f"Process {pid}: {rss} kB")
    print(f"Total memory for {program}: {total} kB")

def print_memory_bar(used, total, bar_length, human_readable=False):
    used_display = f"{used / (1024 ** 2):.2f} GiB" if human_readable else f"{used} kB"
    total_display = f"{total / (1024 ** 2):.2f} GiB" if human_readable else f"{total} kB"
    percent = used / total
    bar = '#' * int(bar_length * percent) + '-' * (bar_length - int(bar_length * percent))
    print(f"Memory [{bar} | {percent:.0%}] {used_display}/{total_display}")

def main():
    parser = argparse.ArgumentParser(description="Monitor memory usage.")
    parser.add_argument("program", nargs="?", help="Program name to analyze")
    parser.add_argument("-H", action="store_true", help="Display memory in human-readable format")
    parser.add_argument("-l", type=int, default=20, help="Length of the memory bar")
    args = parser.parse_args()

    meminfo = read_meminfo()
    if args.program:
        display_program_memory(args.program)
    else:
        used, total = calculate_memory(meminfo)
        print_memory_bar(used, total, args.l, args.H)

if __name__ == "__main__":
    main()
