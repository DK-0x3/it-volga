import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://practice-automation.com/click-events/"


@allure.epic("Practice Automation Demo")
@allure.feature("Click Events")
@allure.story("Кнопки животных")
@allure.title("Проверка кнопок: животное → звук")
@pytest.mark.parametrize(
    "button_text, expected_text",
    [
        ("Cat", "Meow!"),
        ("Dog", "Woof!"),
        ("Pig", "Oink!"),
        ("Cow", "Moo!"),
    ]
)
def test_animal_button_click(browser, button_text, expected_text):
    """
    Проверяет, что при клике на кнопку животного
    в поле <h2 id="demo"> появляется правильный текст.
    """
    wait = WebDriverWait(browser, 5)

    with allure.step("Открываем страницу с кнопками"):
        browser.get(BASE_URL)

    with allure.step(f"Кликаем по кнопке '{button_text}'"):
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{button_text}']"))
        )
        button.click()

    with allure.step(f"Проверяем, что в <h2 id='demo'> появился текст '{expected_text}'"):
        wait.until(EC.text_to_be_present_in_element((By.ID, "demo"), expected_text))
        demo_elem = browser.find_element(By.ID, "demo")
        allure.attach(
            demo_elem.text,
            name=f"Текст после клика на {button_text}",
            attachment_type=allure.attachment_type.TEXT
        )
        assert demo_elem.text == expected_text, (
            f"Для кнопки '{button_text}' ожидалось '{expected_text}', а получили '{demo_elem.text}'"
        )
