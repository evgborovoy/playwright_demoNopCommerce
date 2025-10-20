import pytest
import allure
import os
from playwright.sync_api import sync_playwright
from config.settings import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.helpers import generate_random_email, generate_random_password

IS_CI_HEADLESS = os.environ.get('CI_HEADLESS') == 'true'


@pytest.fixture(scope="session")
def browser():
    headless_mode = True if IS_CI_HEADLESS else Config.HEADLESS
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless_mode,
            timeout=Config.DEFAULT_TIMEOUT
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        base_url=Config.BASE_URL
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def login_page(page, home_page):
    home_page.navigate("")
    if home_page.is_user_logged_in():
        home_page.click_logout()

    login_page = LoginPage(page)
    login_page.navigate("login")
    login_page.wait_for_login_form()
    return login_page


@pytest.fixture
def logged_in_home(login_page, home_page) -> 'HomePage':
    """
    Logs you in and returns the HomePage.
    Tests using this fixture start in the logged in state.
    """
    random_email = generate_random_email()
    random_password = generate_random_password()

    login_page.login(random_email, random_password)

    home_page.wait_for_login_state(should_be_logged_in=True)

    return home_page


@pytest.fixture
def register_page(page, home_page):
    home_page.navigate("")
    if home_page.is_user_logged_in():
        home_page.click_logout()

    register_page = RegisterPage(page)
    register_page.navigate("register")
    register_page.wait_for_register_form()
    return register_page


@pytest.fixture
def products_page(page):
    return ProductsPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def add_product_in_cart(products_page, cart_page):
    """Ensures the cart is empty, adds one product, and clears the cart after the test"""
    products_page.logger.info("SETUP: Clearing cart before adding product.")
    cart_page.navigate("cart")
    cart_page.clear_cart()

    products_page.navigate("/books")
    products_page.wait_for_products()
    product_names = products_page.get_product_names()

    if not product_names:
        pytest.skip("No books available")

    book_name = product_names[0]
    products_page.click_product(book_name)
    added_to_cart = products_page.add_to_cart()

    if not added_to_cart:
        pytest.fail("Failed to add product to cart during fixture setup.")

    yield True

    products_page.logger.info("TEARDOWN: Clearing cart after test.")
    cart_page.navigate("cart")
    cart_page.clear_cart()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure while test failed"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_obj = item.funcargs.get("page")

        if page_obj and hasattr(page_obj, 'screenshot'):
            try:
                screenshot = page_obj.screenshot()
                allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
                html = page_obj.content()
                allure.attach(html, name="page_html", attachment_type=allure.attachment_type.HTML)
                allure.attach(page_obj.url, name="page_url", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                print(f"Could not take screenshot: {e}")
