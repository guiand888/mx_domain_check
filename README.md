✉️ MX Domain Check
===

## Overview

**`mx_domain_check`** is a Python script that reads email addresses from a CSV file, extracts the domain part of each email address, checks the domain's MX (Mail Exchange) records, and identifies if any of them are associated with Google. It then records those domains in a new CSV file named `results.csv`.

## Why?
You use case is yours. Mine is that I do a lot of email marketing outreach and some of the services we offer do not apply to Google Workspace customers.

## Features

- Reads a list of entries (email addresses or domains) from a specified CSV file.
- Extracts the domain from each entry if necessary.
- Checks the domain's MX records using the dig command.
- Identifies domains with MX records that end with google.com.
- Outputs the matched domains to a specified CSV file.
- `-p`: otionally shows a progress indicator updated every 1 second.

## Requirements

- Python 3.x
- `dig` command-line tool (part of the `dnsutils` package on most Unix-like systems)

## Installation

**1. Clone the repository (if applicable):**
```sh
git clone https://github.com/yourusername/mx_domain_check.git
cd mx_domain_check
```

**2. Ensure `dig` is installed on your system:**
On RedHat-based systems (e.g., Fedora):
```sh
sudo yum install bind-utils
```

On Debian-based systems (e.g., Ubuntu):
```sh
sudo apt-get install dnsutils
```

## Usage

**1. Prepare your input file (emails_and_domains.csv) containing email addresses and/or domains, one per line:**

```csv
user1@gmail.com
user2@yahoo.com
businessdomain.com
```

**2. Run the script:**

```sh
python ./mx_domain_check.py -i test_emails_and_domains.csv -o results.csv -p
```

**3.Check the output:**

The script will generate a results.csv file containing the domains whose MX records end with google.com.


## Example

Given an `emails.csv` file with the following content:
```csv
user1@gmail.com
user2@yahoo.com
user3@businessdomain.com
```

The script will perform the following steps:
1. Extract the domains:
    - gmail.com
    - yahoo.com
    - businessdomain.com

2. Check the MX records for each domain:
    - `dig +short gmail.com MX` (expected to find Google MX records)
    - `dig +short yahoo.com MX` (expected not to find Google MX records)
    - `dig +short businessdomain.com MX` (varies)

3. Output matched domains to `results.csv`:
```csv
gmail.com
```

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/feature-name`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature/feature-name`).
5. Create a new Pull Request.

## Author

Guillaume André
