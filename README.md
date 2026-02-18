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
│   ├── test_checkout.py           # Checkout flow tests
│   ├── page_objects_examples.py   # Usage examples
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Page Objects

### HomePage (`home_page.py`)
Converted from the TypeScript HomePage class, provides methods for:
- Navigation and basic page interactions
- Popup/cookie dismissal
- User authentication verification
- Product management (adding to basket, counting products)
- Navigation to other pages (login, basket, sidenav)

**Key Methods:**
- `navigate_sync(url)` - Navigate to a URL
- `dismiss_popup_and_cookies_sync()` - Dismiss welcome banner and cookies
- `open_login_page_sync()` - Open login page via account menu
- `add_product_to_basket_sync(product_name)` - Add product to basket
- `verify_logged_in_sync()` / `verify_user_not_logged_in_sync()` - Check auth status
- `get_visible_products_count_sync()` - Count visible products
- Both sync (`_sync`) and async versions available

### LoginPage (`login_page.py`)
Handles user login functionality:
- Email/password input
- Login button interaction
- Navigation to registration

### RegisterPage (`register_page.py`)
Handles user registration:
- Unique email generation
- Form completion with security questions
- Registration submission

### CheckoutPage (`checkout_page.py`) 
Manages checkout process:
- Checkout initiation
- Address addition with form fields
- Payment flow navigation

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install browsers:
   ```bash
   playwright install
   ```

## Usage Examples

### Basic Navigation
```python
from tests.home_page import HomePage

def test_basic_navigation(page: Page):
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    
    products_count = home_page.get_visible_products_count_sync()
    assert products_count > 0
```

### User Registration & Login
```python
def test_user_flow(page: Page):
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    
    # Register user
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()
    
    register_page = RegisterPage(page)
    email = register_page.register_user_sync()
    
    # Login
    login_page.email_field.fill(email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()
    
    home_page.verify_logged_in_sync()
```

### Shopping Flow
```python
def test_shopping(page: Page):
    # ... login code ...
    
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")
    home_page.verify_basket_items_count_sync(1)
    home_page.open_basket_sync()
    
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()
    checkout_page.add_address_sync()
    checkout_page.proceed_to_payment_sync()
```

## Running Tests

```bash
# Run specific test
python -m pytest tests/test_example.py::test_juice_shop_title -v

# Run all tests
python -m pytest tests/ -v

# Run tests with specific browser
python -m pytest tests/ --browser chromium -v

# Run with headed browser (visible)
python -m pytest --headed
```

## Key Features

1. **Page Object Model**: Clean separation of page logic and test logic
2. **Sync/Async Support**: Both synchronous and asynchronous method versions
3. **Reusable Components**: Common flows abstracted into reusable methods
4. **TypeScript Conversion**: Faithful Python conversion of TypeScript Playwright code
5. **Comprehensive Coverage**: Registration, login, shopping, and checkout flows

## Dependencies

- `pytest-playwright` - Playwright testing framework for Python
- `playwright` - Browser automation library

Install with: `pip install -r requirements.txt`
