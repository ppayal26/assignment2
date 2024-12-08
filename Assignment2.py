#!/usr/bin/env python3
import argparse
import os
import sys

def generate_memory_bar(usage_percentage, max_length=20):
    """Generate a bar to represent memory usage as a percentage."""
    num_hashes = int(usage_percentage * max_length)
    num_spaces = max_length - num_hashes
    return f"[{'#' * num_hashes}{' ' * num_spaces} | {int(usage_percentage * 100)}%]"

def get_total_system_memory():
    """Get the total system memory in kilobytes."""
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                return int(line.split()[1])
    return None

def get_available_memory():
    """Get available system memory from /proc/meminfo."""
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemAvailable'):
                return int(line.split()[1])
    return None

def get_process_ids(program_name):
    """Return a list of process IDs running a specific program."""
    try:
        pids = os.popen(f"pidof {program_name}").read().strip().split()
        return [int(pid) for pid in pids]
    except Exception:
        return []

def get_resident_memory_size(pid):
    """Get the RSS memory size of a process by its PID."""
    try:
        with open(f'/proc/{pid}/statm', 'r') as f:
            return int(f.read().split()[1]) * 4096  # In bytes
    except Exception:
        return 0

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Memory Visualizer')
    parser.add_argument('-H', '--human-readable', action='store_true', help="Display memory in a human-readable format")
    parser.add_argument('-l', '--length', type=int, default=20, help="Graph length (default: 20)")
    parser.add_argume
