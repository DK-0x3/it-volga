import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    # driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук pytest — вызывается после каждого теста.
    Если тест упал, делаем скриншот из браузера и прикрепляем в Allure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")  # берём фикстуру browser
        if browser:
            try:
                screenshot = browser.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Screenshot on failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")