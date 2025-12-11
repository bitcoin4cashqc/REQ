# REQ - Quebec Business Register API Client

A Python client for the Quebec Business Register (Registre des entreprises du Québec) API.

**Note:** This library uses `cloudscraper` to bypass Cloudflare protection on the Quebec Business Register website.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Search

```python
from REQ import REQ, SearchOptions

def main():
    # Using context manager (recommended)
    with REQ() as client:
        # Search for enterprises (use specific search terms)
        options = SearchOptions(keywords="Bombardier")
        results = client.search(options)

        print(f"Total results: {results.TotalEnregistrements}")
        print(f"Pages: {results.NombrePages}")

        for entreprise in results.ListeEntreprises:
            print(f"Name: {entreprise.Nom}")
            print(f"NEQ: {entreprise.NumeroDossier}")
            print(f"Status: {entreprise.Statut}")
            print("---")

if __name__ == "__main__":
    main()
```

### Advanced Search with Pagination

```python
from REQ import REQ, SearchOptions

def main():
    with REQ() as client:
        # Search with additional filters
        options = SearchOptions(
            keywords="tech",
            domain=1,  # Optional domain filter
            type=2,    # Optional type filter
            page=0     # Page number (0-indexed)
        )

        results = client.search(options)

        # Paginate through results
        for page in range(min(3, results.NombrePages)):  # First 3 pages
            options.page = page
            page_results = client.search(options)
            print(f"Page {page + 1}/{results.NombrePages}")
            for entreprise in page_results.ListeEntreprises:
                print(f"  - {entreprise.Nom}")

if __name__ == "__main__":
    main()
```

### Get Enterprise by NEQ

```python
from REQ import REQ

def main():
    with REQ() as client:
        # Get specific enterprise by NEQ number
        neq = "1143920115"  # Bombardier Inc.
        entreprise = client.get_neq(neq)
        print(entreprise)

if __name__ == "__main__":
    main()
```

### Manual Session Management

If you prefer not to use the context manager:

```python
from REQ import REQ, SearchOptions

def main():
    client = REQ()

    try:
        options = SearchOptions(keywords="Bombardier")
        results = client.search(options)
        print(f"Found {results.TotalEnregistrements} results")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

## API Reference

### REQ Class

Main client class for interacting with the Quebec Business Register API.

#### Methods

- `get_neq(neq: str) -> Dict[str, Any]`: Get enterprise information by NEQ number
- `search(options: SearchOptions) -> REQSearchResponse`: Search for enterprises
- `close()`: Close the HTTP session (if not using context manager)

### SearchOptions

Search parameters for enterprise search.

- `keywords: str` (required): Search keywords (avoid overly generic terms)
- `domain: Optional[int]`: Domain filter
- `type: Optional[int]`: Type filter
- `etendue: Optional[int]`: Scope filter
- `page: Optional[int]`: Page number (0-indexed)

### REQSearchResponse

Search response containing:

- `PageCourante: int`: Current page number
- `NombrePages: int`: Total number of pages
- `ListeEntreprises: List[ListeEntreprises]`: List of enterprises
- `TotalEnregistrements: int`: Total number of records
- `CleSession: str`: Session key
- `TypeResultat: str`: Result type
- `Message: str`: Response message (e.g., error messages from API)

### ListeEntreprises

Enterprise information:

- `ID: str`: Enterprise ID
- `NumeroDossier: str`: File number (NEQ)
- `Nom: str`: Name
- `AdressePrimaire: str`: Primary address
- `Statut: str`: Status (e.g., "Immatriculée", "Radiée d'office")
- `DateChangementEtat: str`: Status change date
- `StatutDuNom: str`: Name status
- `DateInitiale: str`: Initial date
- `DateFinale: str`: Final date

## Notes

- The client maintains session state (cookies and session keys) across requests
- Always use `with` statement or remember to call `close()` to properly clean up resources
- The API requires acceptance of terms of use (handled automatically by the client)
- The API uses Cloudflare protection, which is bypassed using `cloudscraper`
- Avoid using overly generic search terms (e.g., "restaurant" alone) as the API will reject them with the message "Ce mot est trop général pour être utilisé seul"
- Search results return a maximum of 25 enterprises per page

## Common Issues

### Search returns empty results

If `ListeEntreprises` is empty and `Message` contains "Ce mot est trop général pour être utilisé seul", your search term is too generic. Try using more specific terms or combinations of words.

### Character encoding

Some characters may appear garbled in the console output (e.g., "Immatricul�e" instead of "Immatriculée"). This is a console encoding issue and does not affect the actual data.
