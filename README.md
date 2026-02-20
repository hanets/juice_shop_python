# Juice Shop Python Automation

This project contains Python Playwright automation tests for the OWASP Juice Shop application, converted from TypeScript using a Page Object Model (POM) architecture.

## Project Structure

```
├── tests/
│   ├── __init__.py                 # Package initialization
│   ├── home_page.py               # HomePage page object
│   ├── login_page.py              # LoginPage page object  
│   ├── register_page.py           # RegisterPage page object
│   ├── checkout_page.py           # CheckoutPage page object
│   ├── test_example.py            # Basic functionality tests
# Juice Shop Python — Playwright tests

Lightweight Playwright-based Python tests for the OWASP Juice Shop demo application. Tests follow a Page Object Model (POM) pattern and live in `page_objects/` and `tests/`.

## Quickstart

1. Create and activate a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install Playwright browsers:

    ```bash
    playwright install
    ```

4. Run tests:

    ```bash
    # Run all tests
    python -m pytest -v

    # Run a single test
    python -m pytest tests/test_example.py::test_juice_shop_title -v
    ```

## Project layout

```
.
├── page_objects/          # Page object classes (HomePage, LoginPage, etc.)
├── tests/                 # pytest test modules
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Notes on tests and page objects

- Page object classes live under `page_objects/` and are imported by tests in `tests/`.
- Tests are written for pytest with Playwright fixtures (see `pytest-playwright`).
- Many page object methods use both synchronous and asynchronous variants — follow existing patterns when adding new helpers.

## Development tips

- Use the project's virtualenv: `source .venv/bin/activate`.
- When adding tests, keep them deterministic and idempotent — create unique test users where required.
- Run Playwright in headed mode for debugging: `pytest --headed`.

## Contributing

If you add features or refactor page objects, please:

1. Keep public method names stable where possible.
2. Add or update tests that exercise the new behavior.
3. Run `python -m pytest -v` before creating a PR.

## Dependencies

- `playwright`
- `pytest-playwright`

Install with `pip install -r requirements.txt`.