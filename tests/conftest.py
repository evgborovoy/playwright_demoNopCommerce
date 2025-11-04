import pytest
import os
from playwright.sync_api import Page

from config.settings import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.helpers import generate_random_email, generate_random_password


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Глобальная настройка контекста для всех тестов:
    - единый viewport
    - locale
    - (опционально) storage_state для reuse login
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 900},
        "locale": "en-US",
        "storage_state": "config/state.json",
        "record_video_dir": "artifacts/videos",
    }


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def login_page(page:Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    RegisterPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def add_product_in_cart(products_page: ProductsPage):
    products_page.navigate_to_computers()
    products_page.navigate_to_desktops()
    first = products_page.get_first_product_name()
    products_page.add_product_to_cart(first)
    yield
