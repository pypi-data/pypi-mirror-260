# Nigerian Bank List (banklist-ng)

The `banklist-ng` library provides information about Nigerian banks including the bank's type, NIP code, name, slug, code, USSD, and logo.

## Usage

### Installation

You can install the package via pip:

```bash
pip install banklist-ng
```

### Importing

```python
from banklist_ng import fetch_banks, filter_banks_by_keyword

# Fetch all banks data
all_banks_data = fetch_banks()
print(all_banks_data)

# Filter banks by keyword
keyword = "Zenith"
zenith_banks = filter_banks_by_keyword(keyword)
print(f"Banks matching '{keyword}':", zenith_banks)
```

### Functions

- `fetch_banks() -> List[BankInfo]`: Fetches a list of all Nigerian banks with their data.

- `filter_banks_by_keyword(keyword: str) -> List[BankInfo]`: Filters banks based on a given keyword in their name property.

### Type Definitions

- `BankInfo`: Represents the data structure for information about a bank, including its ID, type, NIP code, name, slug, code, USSD, and logo.

### JSON Data

The bank data is sourced from a JSON file included with the package. The JSON file contains comprehensive information about each bank.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## GitHub Repository

You can find the source code and contribute to this project on GitHub: [Bank List NG on GitHub](https://github.com/awesomegoodman/banklist-ng)
