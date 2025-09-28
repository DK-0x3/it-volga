import time
import random
import allure

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://practice-automation.com/form-fields/"


@allure.epic("Practice Automation Demo")
@allure.feature("Form Fields")
@allure.story("Позитивный сценарий")
@allure.title("Заполнение всех полей формы и успешная отправка")
@allure.description("Проверка, что при заполнении всех обязательных полей "
                    "форма отправляется и появляется alert с сообщением.")
def test_fill_text_fields_and_submit(browser):
    wait = WebDriverWait(browser, 10)

    with allure.step("Открываем страницу формы"):
        browser.get(BASE_URL)

    with allure.step("Заполняем поле Name"):
        name = browser.find_element(By.ID, "name-input")
        name.clear()
        name.send_keys("Test Name")

    with allure.step("Заполняем поле Password"):
        password = browser.find_element(By.XPATH, "//input[@type='password']")
        password.clear()
        password.send_keys("12345")

    with allure.step("Выбираем все напитки (чекбоксы)"):
        for i in range(1, 6):
            checkbox = browser.find_element(By.ID, f"drink{i}")
            checkbox.click()
            assert checkbox.is_selected()

    with allure.step("Выбираем случайный цвет (radio)"):
        random_index = random.randint(1, 5)
        color_radio = wait.until(EC.element_to_be_clickable((By.ID, f"color{random_index}")))
        color_radio.click()
        assert color_radio.is_selected()

    with allure.step("Перебираем все опции в селекте 'Do you like automation?'"):
        select_elem = Select(browser.find_element(By.ID, "automation"))
        for value in ["yes", "no", "undecided"]:
            select_elem.select_by_value(value)
            selected = select_elem.first_selected_option
            assert selected.get_attribute("value") == value

    with allure.step("Заполняем поле Email"):
        email = browser.find_element(By.ID, "email")
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", email)
        email.clear()
        email.send_keys("textemail@mail.ru")

    with allure.step("Формируем текст сообщения из списка <ul> и заполняем поле Message"):
        tools = browser.find_elements(By.CSS_SELECTOR, "ul li")
        tool_names = [tool.text for tool in tools]
        message_text = "\n".join(tool_names)
        message = browser.find_element(By.ID, "message")
        message.clear()
        message.send_keys(message_text)

    with allure.step("Отправляем форму"):
        submit_btn = wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        time.sleep(1)
        submit_btn.click()

    with allure.step("Проверяем, что появился alert с сообщением"):
        alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
        alert_text = alert.text
        allure.attach(alert_text, name="Alert text", attachment_type=allure.attachment_type.TEXT)
        assert "Thank you" in alert_text or "Message received!" in alert_text
        alert.accept()


@allure.epic("Practice Automation Demo")
@allure.feature("Form Fields")
@allure.story("Radio buttons")
@allure.title("Выбор всех цветов")
@allure.description("Проверка, что каждая радиокнопка цвета (color1...color5) может быть выбрана.")
def test_select_all_colors(browser):
    browser.get(BASE_URL)
    wait = WebDriverWait(browser, 10)

    for i in range(1, 6):
        with allure.step(f"Выбираем цвет color{i}"):
            color_radio = wait.until(EC.element_to_be_clickable((By.ID, f"color{i}")))
            color_radio.click()
            assert color_radio.is_selected(), f"Color {i} не выбран!"


@allure.epic("Practice Automation Demo")
@allure.feature("Form Fields")
@allure.story("Select")
@allure.title("Выбор всех опций в селекте 'Do you like automation?'")
@allure.description("Проверка, что каждую опцию (Yes, No, Undecided) можно выбрать.")
def test_select_automation_options(browser):
    browser.get(BASE_URL)
    select_elem = Select(browser.find_element(By.ID, "automation"))

    option_values = [
        opt.get_attribute("value")
        for opt in select_elem.options
        if opt.get_attribute("value") != "default"
    ]

    for value in option_values:
        with allure.step(f"Выбираем опцию {value}"):
            select_elem.select_by_value(value)
            selected = select_elem.first_selected_option
            assert selected.get_attribute("value") == value


@allure.epic("Practice Automation Demo")
@allure.feature("Form Fields")
@allure.story("Checkboxes")
@allure.title("Выбор всех напитков")
@allure.description("Проверка, что каждый чекбокс drink1...drink5 можно выбрать.")
def test_radio_various_drinks(browser):
    browser.get(BASE_URL)

    for i in range(1, 6):
        with allure.step(f"Выбираем напиток drink{i}"):
            checkbox = browser.find_element(By.ID, f"drink{i}")
            checkbox.click()
            assert checkbox.is_selected()


@allure.epic("Practice Automation Demo")
@allure.feature("Form Fields")
@allure.story("Негативные сценарии")
@allure.title("Отправка формы без заполненного поля Name")
@allure.description("Проверка, что при пустом поле Name alert не появляется, а страница скроллит к Name.")
def test_submit_without_name(browser):
    browser.get(BASE_URL)
    wait = WebDriverWait(browser, 5)

    with allure.step("Очищаем поле Name"):
        name = browser.find_element(By.ID, "name-input")
        name.clear()

    with allure.step("Нажимаем кнопку Submit"):
        submit_btn = wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        time.sleep(1)
        submit_btn.click()

    with allure.step("Проверяем, что alert не появился"):
        alert_appeared = True
        try:
            wait.until(EC.alert_is_present())
        except TimeoutException:
            alert_appeared = False
        assert not alert_appeared, "Alert появился, хотя поле Name пустое!"

    with allure.step("Проверяем, что поле Name в зоне видимости"):
        is_in_viewport = browser.execute_script("""
            var elem = arguments[0];
            var rect = elem.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        """, name)
        assert is_in_viewport, "Поле Name не в зоне видимости после клика Submit"
