import re
import json
import csv
import argparse
from typing import Dict, Any, Tuple, Set

# --- regex for Standalone PII ---
# Pre-compile regex for efficiency
PHONE_REGEX = re.compile(r'\b\d{10}\b')
AADHAR_REGEX = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
PASSPORT_REGEX = re.compile(r'\b[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]\b', re.IGNORECASE)
UPI_REGEX = re.compile(r'[\w\.\-]+@\w+')

# --- regex Combinatorial PII ---
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
IP_ADDRESS_REGEX = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# --- Redaction Functions ---

def redact_phone(phone_str: str) -> str:
    return f"{phone_str[:2]}XXXXXX{phone_str[-2:]}"

def redact_aadhar(aadhar_str: str) -> str:
    return f"XXXXXXXX{aadhar_str.replace(' ', '')[-4:]}"

def redact_passport(passport_str: str) -> str:
    return f"{passport_str[0]}XXXXXX{passport_str[-1]}"

def redact_name(name: str) -> str:
    parts = name.split()
    redacted_parts = [p[0] + 'X' * (len(p) - 1) for p in parts if len(p) > 0]
    return ' '.join(redacted_parts)

def redact_email(email: str) -> str:
    try:
        local_part, domain = email.split('@', 1)
        if len(local_part) > 2:
            redacted_local = f"{local_part[0]}XXX{local_part[-1]}"
        else:
            redacted_local = "X" * len(local_part)
        return f"{redacted_local}@{domain}"
    except ValueError:
        return "[REDACTED_EMAIL]"

def process_record(data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    redacted_data = data.copy()
    is_pii_found = False
    combinatorial_keys: Set[str] = set()
    pii_fields_to_redact: Set[str] = set()

    # --- Step 1: Detect all potential PII and mark for redaction if Standalone ---
    for key, value in data.items():
        if not isinstance(value, str) or not value.strip():
            continue

        # A. Standalone PII Checks
        if PHONE_REGEX.search(value) and key in ['phone', 'contact']:
            is_pii_found = True
            redacted_data[key] = redact_phone(value)
        elif AADHAR_REGEX.search(value) and key in ['aadhar', 'address_proof']:
            is_pii_found = True
            redacted_data[key] = redact_aadhar(value)
        elif PASSPORT_REGEX.search(value) and key in ['passport']:
            is_pii_found = True
            redacted_data[key] = redact_passport(value)
        elif UPI_REGEX.search(value) and key in ['upi_id']:
            # Avoid matching emails by checking domain part simplicity
            if len(value.split('@')[1].split('.')) == 1:
                is_pii_found = True
                redacted_data[key] = "[REDACTED_UPI]"

        # B. Combinatorial PII Identification
        # Identify potential fields but do not redact yet
        elif key == 'name' and len(value.strip().split()) > 1:
            combinatorial_keys.add('name')
        elif EMAIL_REGEX.search(value) and key == 'email':
            combinatorial_keys.add('email')
        elif key == 'address' and len(value.strip()) > 10: # Simple heuristic for a real address
             combinatorial_keys.add('address')
        elif key in ['ip_address', 'device_id']:
            combinatorial_keys.add('device_context')


    # --- Step 2: Evaluate combinatorial logic ---
    if len(combinatorial_keys) >= 2:
        is_pii_found = True
        if 'name' in combinatorial_keys: pii_fields_to_redact.add('name')
        if 'email' in combinatorial_keys: pii_fields_to_redact.add('email')
        if 'address' in combinatorial_keys: pii_fields_to_redact.add('address')
        if 'device_context' in combinatorial_keys:
             pii_fields_to_redact.add('ip_address')
             pii_fields_to_redact.add('device_id')


    # --- Step 3: Redact combinatorial PII fields if condition was met ---
    if pii_fields_to_redact:
        for key in pii_fields_to_redact:
            if key in redacted_data and isinstance(redacted_data[key], str):
                if key == 'name':
                    redacted_data[key] = redact_name(redacted_data[key])
                elif key == 'email':
                    redacted_data[key] = redact_email(redacted_data[key])
                elif key == 'address':
                    redacted_data[key] = "[REDACTED_ADDRESS]"
                else: # ip_address, device_id
                    redacted_data[key] = "[REDACTED_IDENTIFIER]"

    return redacted_data, is_pii_found


def main(input_file: str, output_file: str):
    """
    Main function to read, process, and write CSV data.
    """
    print(f"Starting PII detection for '{input_file}'...")
    processed_records = []

    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                record_id = row['record_id']
                data_json_str = row['data_json']

                try:
                    data = json.loads(data_json_str)
                    redacted_data, is_pii = process_record(data)
                    processed_records.append({
                        'record_id': record_id,
                        'redacted_data_json': json.dumps(redacted_data),
                        'is_pii': is_pii
                    })
                except json.JSONDecodeError:
                    # Handle malformed JSON gracefully
                    processed_records.append({
                        'record_id': record_id,
                        'redacted_data_json': '{"error": "Invalid JSON format"}',
                        'is_pii': False
                    })

        # Write the output file
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            fieldnames = ['record_id', 'redacted_data_json', 'is_pii']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_records)

        print(f"Processing complete. Output saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to detect and redact PII from a CSV file."
    )
    parser.add_argument(
        "input_file",
        help="The path to the input CSV file (e.g., iscp_pii_dataset.csv)."
    )
    # Define a default output file name based on the candidate's name
    default_output_file = "redacted_output_varikuti_narendra_reddy.csv"
    parser.add_argument(
        "-o", "--output_file",
        default=default_output_file,
        help=f"The path to the output CSV file (default: {default_output_file})."
    )
    args = parser.parse_args()

    main(args.input_file, args.output_file)