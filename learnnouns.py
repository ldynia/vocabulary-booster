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
        default='db/nouns.csv',
        help='CSV file (default: nouns.csv)'
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
        eng, lemma, indefin, defin, pl_indefin, pl_defin = word[:last_column]
        print(f"Bydeform: {GREEN}{lemma}{RESET} ({YELLOW}{eng}{RESET})")

        # Get user input
        user_indefin = input('Ental Ubestemt (a): ').strip()
        user_definitive = input('Ental Bestemt (the): ').strip()
        user_pl_indefin = input('Flertal Ubestemt (some): ').strip()
        user_pl_defin = input('Flertal Bestemt (these): ').strip()

        # Mark this word as typed
        typed_words.add(word)
        print()

        success_indefin = True
        success_defin = True
        success_pl_indefin = True
        success_pl_defin = True

        # Print results
        print(f"{YELLOW}{lemma:<12}{RESET}\t\t{'Dit Svar':<12}\t{'Rigtig Svar':<12}")
        print("-" * 54)
        if user_indefin != indefin:
            print(f"{'Ental Ubestemt':<12}\t\t{RED}{user_indefin:<12}{RESET}\t{GREEN}{indefin:<12}{RESET}")
            success_indefin = False
        else:
            print(f"{'Ental Ubestemt':<12}\t\t{GREEN}{user_indefin:<12}{RESET}\t{GREEN}{indefin:<12}{RESET}")

        if user_definitive != defin:
            print(f"{'Ental Bestemt':<12}\t\t{RED}{user_definitive:<12}{RESET}\t{GREEN}{defin:<12}{RESET}")
            success_defin = False
        else:
            print(f"{'Ental Bestemt':<12}\t\t{GREEN}{user_definitive:<12}{RESET}\t{GREEN}{defin:<12}{RESET}")

        if user_pl_indefin != pl_indefin:
            print(f"{'Flertal Ubestemt':<12}\t{RED}{user_pl_indefin:<12}{RESET}\t{GREEN}{pl_indefin:<12}{RESET}")
            success_pl_indefin = False
        else:
            print(f"{'Flertal Ubestemt':<12}\t{GREEN}{user_pl_indefin:<12}{RESET}\t{GREEN}{pl_indefin:<12}{RESET}")

        if user_pl_defin != pl_defin:
            print(f"{'Flertal Bestemt':<12}\t\t{RED}{user_pl_defin:<12}{RESET}\t{GREEN}{pl_defin:<12}{RESET}")
            success_pl_defin = False
        else:
            print(f"{'Flertal Bestemt':<12}\t\t{GREEN}{user_pl_defin:<12}{RESET}\t{GREEN}{pl_defin:<12}{RESET}")

        # Determine output file based on success
        used_file = "tmp/" + used_file[used_file.index('/') + 1:]
        if all([success_indefin, success_defin, success_pl_indefin, success_pl_defin]):
            successes += 1
            outputfile = used_file.replace('.csv', '_successful.csv')
        else:
            failures += 1
            misspelled_words.append(lemma)
            outputfile = used_file.replace('.csv', '_misspelled.csv')

        # Read existing rows (if any) to avoid duplicates
        existing_rows = set()
        file_has_content = (os.path.exists(outputfile) and os.path.getsize(outputfile) > 0)
        if file_has_content:
            with open(outputfile, mode='r', encoding='utf-8') as rf:
                rdr = csv.reader(rf)
                next(rdr, None)  # skip header
                for r in rdr:
                    existing_rows.add(tuple(r))

        row = (eng, lemma, indefin, defin, pl_indefin, pl_defin)
        if row not in existing_rows:
            # Write header only when file doesn't exist or is empty
            write_header = not file_has_content

            # Append new missed row
            with open(outputfile, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow([
                        "English",
                        "Navneform",
                        "Ental Ubestemt",
                        "Ental Bestemt",
                        "Flertal Ubestemt",
                        "Flertal Bestemt"
                    ])
                writer.writerow(list(row))
        print()

    print(f"Successful answers: {successes}")
    print(f"Missed answers: {failures}")
    print(f"Misspelled words: {', '.join(misspelled_words)}")