from dataclasses import dataclass
from typing import Any, Generator
from playwright.sync_api import Page, expect, APIRequestContext, Playwright
import pytest
from .home_page import HomePage
from .login_page import LoginPage
from .register_page import RegisterPage
from .checkout_page import CheckoutPage
import json
import re
import pandas as pd


def load_checkout_items():
    df = pd.read_csv("tests/checkout_items.csv")
    return [tuple(row) for row in df.values]

@pytest.mark.parametrize("item_name,quantity,price", load_checkout_items())
def test_checkout_with_item_data(page: Page, item_name, quantity, price):
    """Test checkout flow using item data from CSV"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()
    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()
    home_page.verify_logged_in_sync()
    # Add product to basket with quantity (assuming method supports quantity)
    for _ in range(int(quantity)):
        home_page.add_product_to_basket_sync(item_name)
    home_page.open_basket_sync()
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()
    checkout_page.add_address_sync()
    # Optionally verify price, etc.


txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())
json.dumps


@dataclass
class User:
    name: str
    age: int


import heapq


def minCost(arr: list):
    # code here
    if len(arr) <= 1:
        return 0
    heapq.heapify(arr)
    cost = 0
    while len(arr) > 1:
        last_sum = heapq.heappop(arr) + heapq.heappop(arr)
        heapq.heappush(arr, last_sum)
        cost += last_sum

    return cost


def test_min_cost():
    assert minCost([4, 2, 7, 6, 9]) == 62


class Solution:
    def subarraySum[T](self, arr: list[T], *, target: T) -> list[int]:
        size = len(arr)
        sum_arr = []
        for start_index in range(size):
            # sum = arr[start_index]
            next_index = start_index + 1
            if len(sum_arr) > next_index:
                sum_next = sum_arr[next_index]
            else:
                sum_next = 0

                target_diff = target - arr[start_index]
                while sum_next < target_diff and next_index < size:
                    sum_next += arr[next_index]
                    next_index += 1
            if sum_next == target_diff:
                return [start_index + 1, next_index]
            sum_arr.append(sum_next)
        return [-1]

    def relativeSort(self, a1, a2):
        # code here
        dict_res = {}
        ascen = []
        for value in a2:
            dict_res[value] = 0

        for value in a1:
            if value in dict_res:
                dict_res[value] += 1
            else:
                ascen.append(value)
        res = []
        for key, value in dict_res.items():
            for _ in range(value):
                res.append(key)
        res.extend(sorted(ascen))

        mp = {}
        a1.sort(key=lambda x: (mp.get(x, float("inf")), x))
        return res


def toBinary(n):
    # Your code here
    s = ""
    while n:
        s += "1" if (n & 1) else "0"
        n >>= 1
    return s[::-1]


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        # base_url="https://api.github.com", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


def test_full_checkout_flow(page: Page, api_request_context: APIRequestContext):
    res = api_request_context.get("http://localhost:3000/rest/languages")
    res_json = res.json()
    prices: list[int] = [10.5, 2.99, 5, "sd"]
    print(prices)
    user_counts: dict[str, int | float | None] = {
        "admin": 1,
        "guest": 42.5,
        "registered": None,
    }
    toBinary(10)
    u1 = User(age=30, name="Alice")
    v1 = vars(u1)
    print(Solution().subarraySum([26, 3, 28, 7], target=52))
    print(Solution().relativeSort([2, 1, 2, 5, 7, 1, 9, 3, 6, 8, 8], [2, 1, 8, 3]))
    print(f"'GeeksforGeeks'".lower())
    print(f"""Geeks"for"Geeks""".find)
    print(f"""Geeks'for'Geeks""")
    values = ["one", "two", "three"]
    values.append("four")
    values.pop
    values.insert(1, "two and a half")
    values.append
    my_set = set(values)
    my_set.add("five")
    my_set.add("two")
    my_set.discard

    print(my_set)
    my_dict = {"one": 1, "two": 2, "three": 3}
    my_dict["four"] = 4
    my_dict.items

    for key, value in my_dict.items():
        print(f"{key}: {value}")

    if "two" in my_dict and my_dict["two"] == 2:
        print("Two is in the dictionary and its value is 2")

    if my_dict.get("nonexistent_key") == 2:
        print("This won't print because the key doesn't exist")

    x = lambda a, b: a + b
    print(x(5, 3))
    if not (one_value := my_dict.get("one")) == 1:
        raise ValueError(f"One should not be 1, but got {one_value}")

    list(filter(lambda x: x.startswith("t"), values))

    upper_values = [value.upper() for value in values]

    use_map = {"one": 1, "two": 2, "three": 3}
    use_map.get("one")
    number: int = 5
    number = 10
    print(number)
    number = "abc"
    print(number)

    """Test complete checkout flow: register -> login -> add product -> checkout -> add address"""
    # Initialize page objects
    home_page = HomePage(page)

    # Navigate to homepage and dismiss popups
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Go to login page and then register
    login_page = home_page.open_login_page_sync()
    register_page = RegisterPage(page)
    login_page.register_link.click()

    # Register new user
    unique_email = register_page.register_user_sync()

    # Login with the registered user
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()

    # Verify user is logged in
    home_page.verify_logged_in_sync()

    # Add product to basket
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")

    # Open basket and proceed to checkout
    home_page.open_basket_sync()

    # Initialize checkout page and complete checkout flow
    checkout_page = CheckoutPage(page)
    checkout_page.checkout_sync()
    checkout_page.add_address_sync()
    # checkout_page.proceed_to_payment_sync()


def test_register_user(page: Page):
    """Test user registration flow"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Go to registration
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()

    # Register new user
    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()

    # Verify registration was successful by checking we can login
    login_page = LoginPage(page)
    expect(login_page.email_field).to_be_visible()
    s = "Hello, World!"
    for i in range(len(s) // 2):
        start = s[i]
        end = s[len(s) - 1 - i]
        print(start, end)
        if not start == end:
            return False
    return True


def test_add_multiple_products(page: Page):
    """Test adding multiple products to basket after login"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Register and login user
    login_page = home_page.open_login_page_sync()
    login_page.register_link.click()

    register_page = RegisterPage(page)
    unique_email = register_page.register_user_sync()

    # Login
    login_page = LoginPage(page)
    login_page.email_field.fill(unique_email)
    login_page.password_field.fill("123456")
    login_page.login_button.click()

    # Add product to basket
    home_page.add_product_to_basket_sync("Apple Juice (1000ml)")

    # Verify basket has items
    home_page.verify_basket_items_count_sync(1)


def test_product_visibility(page: Page):
    """Test that products are visible on the homepage"""
    home_page = HomePage(page)
    home_page.navigate_sync("http://localhost:3000/#/")
    home_page.dismiss_popup_and_cookies_sync()

    # Verify products are visible
    products_count = home_page.get_visible_products_count_sync()
    assert products_count > 0, "Should have visible products on homepage"
