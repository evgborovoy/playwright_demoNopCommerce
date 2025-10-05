import pytest
import allure
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
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
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

@pytest.fixture
def add_product_in_cart(products_page):
    products_page.navigate("/books")
    products_page.wait_for_products()
    product_names = products_page.get_product_names()
    products_page.logger.info(f"Available books: {product_names}")
    if not product_names:
        pytest.skip("No books available")
    book_name = product_names[0]
    products_page.logger.info(f"Testing with book: {book_name}")
    products_page.click_product(book_name)
    added_to_cart = products_page.add_to_cart()
    return added_to_cart


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure while test failed"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_obj = None
        for fixture_name in item.funcargs:
            if fixture_name == "page":
                page_obj = item.funcargs[fixture_name]
                break

        if page_obj and hasattr(page_obj, 'screenshot'):
            try:
                # Делаем скриншот и прикрепляем к Allure
                screenshot = page_obj.screenshot()
                allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)

                # Также добавляем HTML страницу
                html = page_obj.content()
                allure.attach(html, name="page_html", attachment_type=allure.attachment_type.HTML)

                # Добавляем URL страницы
                allure.attach(page_obj.url, name="page_url", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                print(f"Could not take screenshot: {e}")
