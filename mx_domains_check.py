#!/usr/bin/env python3

import csv
import subprocess
import argparse
import threading
import time

def read_entries_from_csv(file_path):
    entries = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            entries.append(row[0])
    return entries

def extract_domain(entry):
    if '@' in entry:
        return entry.split('@')[1]
    return entry

def get_mx_records(domain):
    result = subprocess.run(['dig', '+short', f'{domain}', 'MX'], capture_output=True, text=True)
    return result.stdout.splitlines()

def check_google_mx(mx_records):
    for record in mx_records:
        if record.endswith('google.com.'):
            return True
    return False

def progress_indicator(total_items, processed_items, stop_event):
    while not stop_event.is_set():
        if total_items > 0:
            progress = 100 * processed_items[0] / total_items
            print(f"Progress: {progress:.2f}%")
        time.sleep(1)
    if total_items > 0:
        progress = 100 * processed_items[0] / total_items
        print(f"Progress: {progress:.2f}%")  # Print final progress when stopping

def main(input_csv, output_csv, show_progress):
    entries = read_entries_from_csv(input_csv)
    total_items = len(entries)
    processed_items = [0]
    stop_event = threading.Event()

    if show_progress:
        # Start the progress indicator thread
        progress_thread = threading.Thread(target=progress_indicator, args=(total_items, processed_items, stop_event))
        progress_thread.start()

    try:
        domains_checked = set()
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for entry in entries:
                domain = extract_domain(entry)
                if domain not in domains_checked:
                    domains_checked.add(domain)
                    mx_records = get_mx_records(domain)
                    if check_google_mx(mx_records):
                        writer.writerow([domain])
                processed_items[0] += 1

    finally:
        if show_progress:
            stop_event.set()
            progress_thread.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check MX records for Google domains.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file with email addresses and/or domains')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file for results')
    parser.add_argument('-p', '--progress', action='store_true', help='Show progress indicator')

    args = parser.parse_args()

    main(args.input, args.output, args.progress)
