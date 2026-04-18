import json
import os
import random
import string
import hashlib
from datetime import datetime

DATA_FILE = "vault_data.json"
LOG_FILE = "activity_log.txt"


class VaultEntry:
    def __init__(self, site, username, password_hash, password_strength, created_at=None):
        self.site = site
        self.username = username
        self.password_hash = password_hash
        self.password_strength = password_strength
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "site": self.site,
            "username": self.username,
            "password_hash": self.password_hash,
            "password_strength": self.password_strength,
            "created_at": self.created_at,
        }


def log_activity(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        log_activity(f"Error loading data: {error}")
        print("There was a problem reading the saved vault data. A new empty vault will be used.")
        return []


def save_data(entries):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(entries, file, indent=4)
    except OSError as error:
        log_activity(f"Error saving data: {error}")
        print("Unable to save vault data right now.")


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_password(length=14):
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_-+=?"
    return "".join(random.choice(charset) for _ in range(length))


def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Moderate"
    return "Strong"


def add_entry(entries):
    site = input("Enter the site or app name: ").strip()
    username = input("Enter the username or email: ").strip()

    if not site or not username:
        print("Site and username cannot be blank.")
        return

    choice = input("Generate a password automatically? (y/n): ").strip().lower()

    if choice == "y":
        while True:
            try:
                length = int(input("Enter desired password length (8-32): "))
                if 8 <= length <= 32:
                    password = generate_password(length)
                    break
                print("Please enter a number between 8 and 32.")
            except ValueError:
                print("Please enter a valid whole number.")
    else:
        password = input("Enter the password to store securely: ").strip()

    if not password:
        print("Password cannot be blank.")
        return

    strength = check_password_strength(password)
    entry = VaultEntry(site, username, hash_password(password), strength)
    entries.append(entry.to_dict())
    save_data(entries)
    log_activity(f"Added entry for site: {site}")

    print("\nEntry added successfully.")
    print(f"Password strength: {strength}")
    if choice == "y":
        print(f"Generated password: {password}")
        print("Save this password somewhere safe because only its hash is stored in the vault.")


def view_entries(entries):
    if not entries:
        print("No entries found in the vault.")
        return

    print("\nSaved Vault Entries")
    print("-" * 60)
    for index, entry in enumerate(entries, start=1):
        print(f"{index}. Site: {entry['site']}")
        print(f"   Username: {entry['username']}")
        print(f"   Strength: {entry['password_strength']}")
        print(f"   Created: {entry['created_at']}")
        print(f"   Password Hash: {entry['password_hash'][:20]}...")
        print("-" * 60)


def search_entries(entries):
    if not entries:
        print("The vault is empty.")
        return

    term = input("Enter a site or username to search for: ").strip().lower()
    matches = [
        entry for entry in entries
        if term in entry["site"].lower() or term in entry["username"].lower()
    ]

    if not matches:
        print("No matching entries found.")
        return

    print("\nSearch Results")
    print("-" * 60)
    for entry in matches:
        print(f"Site: {entry['site']}")
        print(f"Username: {entry['username']}")
        print(f"Strength: {entry['password_strength']}")
        print(f"Created: {entry['created_at']}")
        print("-" * 60)


def delete_entry(entries):
    if not entries:
        print("The vault is empty.")
        return

    view_entries(entries)
    try:
        choice = int(input("Enter the entry number to delete: "))
        if 1 <= choice <= len(entries):
            removed = entries.pop(choice - 1)
            save_data(entries)
            log_activity(f"Deleted entry for site: {removed['site']}")
            print("Entry deleted successfully.")
        else:
            print("Invalid entry number.")
    except ValueError:
        print("Please enter a valid whole number.")


def export_report(entries):
    report_name = "security_report.txt"
    try:
        with open(report_name, "w", encoding="utf-8") as report:
            report.write("CyberSafe Vault Security Report\n")
            report.write("=" * 35 + "\n")
            report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Total entries: {len(entries)}\n\n")

            weak = sum(1 for entry in entries if entry["password_strength"] == "Weak")
            moderate = sum(1 for entry in entries if entry["password_strength"] == "Moderate")
            strong = sum(1 for entry in entries if entry["password_strength"] == "Strong")

            report.write(f"Weak passwords: {weak}\n")
            report.write(f"Moderate passwords: {moderate}\n")
            report.write(f"Strong passwords: {strong}\n\n")

            report.write("Detailed Entries\n")
            report.write("-" * 35 + "\n")
            for entry in entries:
                report.write(f"Site: {entry['site']}\n")
                report.write(f"Username: {entry['username']}\n")
                report.write(f"Strength: {entry['password_strength']}\n")
                report.write(f"Created: {entry['created_at']}\n")
                report.write("-" * 35 + "\n")

        log_activity("Exported security report")
        print(f"Report exported successfully as {report_name}.")
    except OSError as error:
        log_activity(f"Error exporting report: {error}")
        print("Unable to export the report right now.")


def show_menu():
    print("\nCyberSafe Vault")
    print("1. Add a new vault entry")
    print("2. View all entries")
    print("3. Search entries")
    print("4. Delete an entry")
    print("5. Export security report")
    print("6. Exit")


def main():
    entries = load_data()
    log_activity("Program started")

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_entry(entries)
        elif choice == "2":
            view_entries(entries)
        elif choice == "3":
            search_entries(entries)
        elif choice == "4":
            delete_entry(entries)
        elif choice == "5":
            export_report(entries)
        elif choice == "6":
            log_activity("Program ended")
            print("Thank you for using CyberSafe Vault.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
