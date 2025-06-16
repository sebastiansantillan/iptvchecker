#!/usr/bin/env python3
"""
Command-line interface for IPTV Checker
"""

import sys
from iptvchecker import check_playlist

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m iptvchecker <path_to_m3u_file>")
        return

    file_path = sys.argv[1]
    print("Loading channels...")
    
    results = check_playlist(file_path)
    if not results:
        return

    print(f"\nFound {results['total']} channels")
    print("\nChecking channels...")
    
    print("\nResults:")
    print("-" * 80)
    
    for result in results['results']:
        status_prefix = "✓" if "Working" in result['status'] else "✗"
        print(f"{status_prefix} {result['name']}")
        print(f"  URL: {result['url']}")
        print(f"  Status: {result['status']}")
        print("-" * 80)
    
    print(f"\nSummary:")
    print(f"Total channels: {results['total']}")
    print(f"Working channels: {results['working']['count']} (saved to {results['working']['file']})")
    print(f"Non-working channels: {results['not_working']['count']} (saved to {results['not_working']['file']})")

if __name__ == "__main__":
    main()
