# Alex Search

Alex Search is a command-line tool for searching and retrieving paper information using the OpenAlex API.

## Features

- Search for papers based on various criteria such as author, publication year, and keywords.
- Export search results to JSON, CSV, Zotero, or other formats.
- Generate summary statistics and reports based on retrieved data.

## Installation

You can install Alex Search using pip:

```bash
pip install alex-search
```

## Usage Example

. code-block:: bash

    alex-search search [OPTIONS] "Machine learning for fun"

```
Options:

- ``--author``: Filter search results by specific author(s).
- ``--journal``: Filter search results by specific journal(s).
- ``--cited-by``: Filter search results by the number of times the paper has been cited by other papers.
- ``--cited``: Filter search results by the number of times the paper has cited other papers.
- ``--limit``: Limit the number of search results returned.
```
