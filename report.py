"""Create an offline Markdown verification report from an explicit CSV schema."""
import argparse
import csv
import html
import io
from collections import Counter
from pathlib import Path

COLUMNS = ['id', 'test', 'expected', 'observed', 'status', 'evidence']
STATUSES = {'PASS', 'FAIL', 'PENDING'}


def read_results(text):
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')))
    if reader.fieldnames != COLUMNS:
        raise ValueError('CSV columns must be: ' + ','.join(COLUMNS))
    records = []
    seen = set()
    for number, raw in enumerate(reader, 2):
        if None in raw or any(value is None for value in raw.values()):
            raise ValueError(f'Row {number}: incorrect field count')
        row = {key: value.strip() for key, value in raw.items()}
        row['status'] = row['status'].upper()
        if row['status'] not in STATUSES:
            raise ValueError(f'Row {number}: status must be PASS, FAIL or PENDING')
        if not all(row[key] for key in ['id', 'test', 'expected']):
            raise ValueError(f'Row {number}: id, test and expected are required')
        if row['id'] in seen:
            raise ValueError(f'Row {number}: duplicate id')
        if row['status'] != 'PENDING' and not row['observed']:
            raise ValueError(f'Row {number}: executed tests need an observation')
        seen.add(row['id'])
        records.append(row)
    if not records:
        raise ValueError('CSV must contain at least one test')
    return records


def cell(value):
    value = html.escape(value, quote=False).replace('\\', '&#92;')
    for character in ['|', '`', '*', '_', '[', ']']:
        value = value.replace(character, f'&#{ord(character)};')
    return value.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>')


def render(records):
    counts = Counter(row['status'] for row in records)
    lines = ['# Network Verification Report', '',
             'Generated from user-entered CSV records. Statuses are not independently verified.', '',
             f"Total: {len(records)} | PASS: {counts['PASS']} | FAIL: {counts['FAIL']} | PENDING: {counts['PENDING']}", '',
             '| ID | Test | Expected | Observed | Status | Evidence reference |',
             '|---|---|---|---|---|---|']
    for row in records:
        lines.append('| ' + ' | '.join(cell(row[key]) for key in COLUMNS) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        records = read_results(args.csv_file.read_text(encoding='utf-8-sig'))
        report = render(records)
        # Exclusive creation preserves existing files and prevents concurrent overwrite.
        with args.output.open('x', encoding='utf-8') as output:
            output.write(report)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
