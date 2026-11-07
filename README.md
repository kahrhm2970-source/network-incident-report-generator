# Network Incident Report Generator

An educational Python automation project by **Alhussin Abutalib**, prepared with AI assistance to support an IT Support and networking portfolio.

## Purpose
Turn manually recorded network verification results into a consistent Markdown report. This continues the [Network Troubleshooting Casebook](https://github.com/kahrhm2970-source/network-troubleshooting-casebook) by separating expected behavior, actual observations, test status, and evidence references.

## Features
- Local CSV input and Markdown output, using only the Python standard library.
- PASS / FAIL / PENDING counts. Pending tests remain pending.
- Required fields, unique test IDs, supported statuses, and observations for executed tests are validated.
- Arabic and UTF-8 BOM support.
- Table content is escaped to reduce unintended Markdown/HTML formatting.
- Existing output files are protected from overwrite.

## Requirements and usage
Python 3.9 or newer. No packages, credentials, or network connections are required.

```bash
git clone https://github.com/kahrhm2970-source/network-incident-report-generator.git
cd network-incident-report-generator
python report.py sample.csv -o my-report.md
python -m unittest -v
```

Choose a new output filename each time. The output parent folder must already exist. Exit 0 means report generation succeeded, even if some tests are marked FAIL. Input/output or validation errors exit with code 2.

## CSV schema
Columns must appear in this exact order.

```csv
id,test,expected,observed,status,evidence
INC-001,Staff DHCP,VLAN 10 address,,PENDING,
```

ID, test, and expected are required. Status is case-insensitive. PASS and FAIL require a nonempty observed field. Evidence is an optional text reference, not an embedded file or verified URL. Quote CSV fields containing commas or newlines.

## Example and actual validation
[sample.csv](sample.csv) contains **synthetic demonstration data**, with one PASS, one FAIL, and one PENDING. These are not results from a real device or Packet Tracer run. [sample-report.md](sample-report.md) is the actual output produced by running the generator on that sample.

Seven unit tests passed locally, covering summaries, pending results, missing observations, duplicate IDs, malformed inputs, escaping, and Arabic/BOM input. An additional CLI check confirmed that an existing report was preserved and a second write exited with code 2.

## Using the casebook
1. Execute a casebook lab and record actual observations.
2. Create a sanitized CSV with the schema above.
3. Use PENDING for tests not yet executed; never substitute an expected result for an observation.
4. Generate the Markdown report.
5. Review the report and evidence references before publication.

## Limits and lessons
The generator trusts the status entered by the operator. It does not execute pings, infer pass/fail from prose, verify evidence, or determine root cause. Tests on actual network incidents remain a future validation step. The implementation illustrates explicit validation, reproducible output, preserving unknown results, and protecting existing files.

## Files
- report.py — command-line application.
- test_report.py — seven unit tests.
- sample.csv — clearly labeled demonstration input.
- sample-report.md — generated demonstration report.
- .gitignore — local/private data exclusions.

## Privacy
Keep real reports in private/ or another untracked location. Remove customer identifiers, real infrastructure addresses, credentials, and secrets before sharing. Gitignore does not remove data already committed.

## Contact
[LinkedIn](https://www.linkedin.com/in/alhussin-abutalib-02696a416/) · [GitHub](https://github.com/kahrhm2970-source)

## References
[Python csv](https://docs.python.org/3/library/csv.html) · [Python unittest](https://docs.python.org/3/library/unittest.html)
