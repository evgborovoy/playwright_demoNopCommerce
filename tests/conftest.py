import pytest
from playwright.sync_api import Page

from config.settings import Config
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.cart_page import CartPage
from pages.products_page import ProductsPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": Config.BASE_URL,
        "viewport": {"width": 1366, "height": 900},
        "locale": "en-US",
        "user_agent": Config.USER_AGENT,
    }


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def add_product_in_cart(products_page: ProductsPage):
    products_page.navigate_to_computers()
    products_page.navigate_to_software()
    first = products_page.get_first_product_name()
    products_page.add_product_to_cart(first)
    yield
