import csv
import random
import argparse
import os
import sys
from typing import List, Tuple


GREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'

successes = 0
failures = 0
misspelled_words = []


def load_csv(file_path: str) -> List[Tuple[str]]:
    entries: List[Tuple[str]] = []
    with open(file_path, mode='r', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        next(reader, None)  # skip header
        for rec in reader:
            entries.append(tuple(rec))
    return entries


def get_unique_word(words: List[Tuple[str]], used: set) -> Tuple[str]:
    remaining_words = [word for word in words if word not in used]
    return random.choice(remaining_words) if remaining_words else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Booster")
    parser.add_argument(
        'filename',
        nargs='?',
        default='db/verbs.csv',
        help='CSV file (default: verbs.csv)'
    )

    args = parser.parse_args()

    # Determine which file to use
    supplied = args.filename
    default_file = parser.get_default('filename')
    used_file = default_file
    if supplied != default_file:
        used_file = supplied

    # Check if file exists
    if not os.path.isfile(used_file):
        print(f"Error: File '{used_file}' not found.")
        sys.exit(1)

    # Load dataset
    dataset = load_csv(used_file)
    typed_words = set()
    print(f"Loaded {len(dataset)} words from '{used_file}'.")

    while len(typed_words) != len(dataset):
        word = get_unique_word(dataset, typed_words)
        last_column = len(word)
        eng, stem, infi, present, past, perfekt = word[:last_column]
        print(f"Udsagnsord: {GREEN}{infi}{RESET} ({YELLOW}{eng}{RESET})")

        # Get user input
        user_stem = input('Bydeform: ').strip()
        user_present = input('Nutid: ').strip()
        user_past = input('Datid: ').strip()
        user_perfekt = input('Perfektum: ').strip()

        # Mark this word as typed
        typed_words.add(word)
        print()

        success_imper = True
        success_present = True
        success_past = True
        success_perfekt = True

        # Print results
        print(f"{YELLOW}{infi:<12}{RESET} {'Dit Svar':<12} {'Rigtig Svar':<12}")
        print("-" * 40)
        if user_stem != stem:
            print(f"{'Bydeform':<12} {RED}{user_stem:<12}{RESET} {GREEN}{stem:<12}{RESET}")
            success_imper = False
        else:
            print(f"{'Bydeform':<12} {GREEN}{user_stem:<12}{RESET} {GREEN}{stem:<12}{RESET}")

        if user_present != present:
            print(f"{'Nutid':<12} {RED}{user_present:<12}{RESET} {GREEN}{present:<12}{RESET}")
            success_present = False
        else:
            print(f"{'Nutid':<12} {GREEN}{user_present:<12}{RESET} {GREEN}{present:<12}{RESET}")

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

        # Determine output file based on success
        used_file = "tmp/" + used_file[used_file.index('/') + 1:]
        if all([success_imper, success_present, success_past, success_perfekt]):
            successes += 1
            misspells = used_file.replace('.csv', '_successful.csv')
        else:
            failures += 1
            misspelled_words.append(infi)
            misspells = used_file.replace('.csv', '_misspelled.csv')

        # Read existing rows (if any) to avoid duplicates
        existing_rows = set()
        file_has_content = (os.path.exists(misspells) and os.path.getsize(misspells) > 0)
        if file_has_content:
            with open(misspells, mode='r', encoding='utf-8') as rf:
                rdr = csv.reader(rf)
                next(rdr, None)  # skip header
                for r in rdr:
                    existing_rows.add(tuple(r))

        row = (eng, stem, infi, present, past, perfekt)
        if row not in existing_rows:
            # Write header only when file doesn't exist or is empty
            write_header = not file_has_content

            # Append new missed row
            with open(misspells, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow([
                        "English",
                        "Bydeform",
                        "Navneform",
                        "Nutid",
                        "Datid",
                        "Perfektum",
                    ])
                writer.writerow(list(row))
        print()

    print(f"Successful answers: {successes}")
    print(f"Missed answers: {failures}")
    print(f"Misspelled words: {', '.join(misspelled_words)}")