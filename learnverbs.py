import csv
import random
import argparse
import os
import sys
from typing import List, Tuple


DB_DIR = 'db'
GREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'


def load_csv(file_path: str) -> List[Tuple[str, ...]]:
    entries: List[Tuple[str, ...]] = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            entries.append(tuple(row))
    return entries


def get_random_word(words: List[Tuple[str, ...]]) -> Tuple[str, ...]:
    return random.choice(words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Booster")
    parser.add_argument(
        'filename',
        nargs='?',
        default='udsagnsord.csv',
        help='CSV file (default: udsagnsord.csv)'
    )

    args = parser.parse_args()

    supplied = args.filename
    default_file = parser.get_default('filename')
    if supplied == default_file:
        used_file = default_file
    else:
        used_file = supplied

    if not os.path.isfile(f"{DB_DIR}/{used_file}"):
        print(f"Error: File '{DB_DIR}/{used_file}' not found.")
        sys.exit(1)

    words = load_csv(f"{DB_DIR}/{used_file}")

    while True:
        eng, infi, stem, imper, present, past, perfekt = get_random_word(words)[0:7]
        print(f"Infinitiv: {GREEN}{infi}{RESET} ({BLUE}{eng}{RESET})")
        
        # Get user input
        user_imper = input('Imperative: ')
        user_present = input('Præsens: ')
        user_past = input('Datid: ')
        user_perfekt = input('Perfektum: ')
        print()

        success_imper = True
        success_present = True
        success_past = True
        success_perfekt = True

        # Print results
        print(f"{'Form':<12} {'Your Answer':<12} {'Correct Answer':<12}")
        print("-" * 40)
        if user_imper != imper:
            print(f"{'Imperative':<12} {RED}{user_imper:<12}{RESET} {GREEN}{imper:<12}{RESET}")
            success_imper = False
        else:
            print(f"{'Imperative':<12} {GREEN}{user_imper:<12}{RESET} {GREEN}{imper:<12}{RESET}")
        
        if user_present != present:
            print(f"{'Præsens':<12} {RED}{user_present:<12}{RESET} {GREEN}{present:<12}{RESET}")
            success_present = False
        else:
            print(f"{'Præsens':<12} {GREEN}{user_present:<12}{RESET} {GREEN}{present:<12}{RESET}")
        
        if user_past != past:
            print(f"{'Datid':<12} {RED}{user_past:<12}{RESET} {GREEN}{past:<12}{RESET}")
            success_past = False
        else:
            print(f"{'Datid':<12} {GREEN}{user_past:<12}{RESET} {GREEN}{past:<12}{RESET}")
        
        if user_perfekt != perfekt:
            print(f"{'Perfektum':<12} {RED}{user_perfekt:<12}{RESET} {GREEN}{perfekt:<12}{RESET}")
            success_perfekt = False
        else:
            print(f"{'Perfektum':<12} {GREEN}{user_perfekt:<12}{RESET} {GREEN}{perfekt:<12}{RESET}")
        
        # Add misspeled words to misspelled list
        if not all([success_imper, success_present, success_past, success_perfekt]):
            miss_file = f"{DB_DIR}/misspelled_{used_file}"
            
            # Do not write header if file exists and is not empty
            write_header = True
            if os.path.exists(miss_file) and os.path.getsize(miss_file) > 0:
                write_header = False
            
            # Write to misspelled file (header only once)
            with open(miss_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(["English", "Infinitiv", "Stem", "Imperative", "Præsens", "Datid", "Perfektum"])
                writer.writerow([eng, infi, stem, imper, present, past, perfekt])
        print()
