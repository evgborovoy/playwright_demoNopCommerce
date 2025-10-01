import pytest
from playwright.sync_api import sync_playwright
from config.settings import Config


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def home_page(page):
    from pages.home_page import HomePage
    return HomePage(page)


@pytest.fixture
def login_page(page):
    from pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture
def register_page(page):
    from pages.register_page import RegisterPage
    return RegisterPage(page)


@pytest.fixture
def products_page(page):
    from pages.products_page import ProductsPage
    return ProductsPage(page)


@pytest.fixture
def cart_page(page):
    from pages.cart_page import CartPage
    return CartPage(page)
