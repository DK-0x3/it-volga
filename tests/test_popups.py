import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://practice-automation.com/popups/"


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Alert Popup")
@allure.title("Проверка кнопки 'Alert Popup'")
@allure.description("При клике на кнопку 'Alert Popup' появляется JS-alert с текстом "
                    "'Hi there, pal!', который можно закрыть.")
def test_alert_popup(browser):
    wait = WebDriverWait(browser, 5)

    with allure.step("Открываем страницу с попапами"):
        browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Alert Popup'"):
        alert_button = wait.until(
            EC.element_to_be_clickable((By.ID, "alert"))
        )
        alert_button.click()

    with allure.step("Проверяем, что появился alert с правильным текстом"):
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        allure.attach(alert_text, name="Alert text", attachment_type=allure.attachment_type.TEXT)
        assert alert_text == "Hi there, pal!"

    with allure.step("Закрываем alert нажатием OK"):
        alert.accept()


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Confirm Popup")
@allure.title("Confirm Popup — нажатие кнопки Да")
@allure.description("При клике на кнопку 'Confirm Popup' появляется диалог с кнопками OK/Cancel. "
                    "Если нажать OK — в блоке #confirmResult появляется текст 'OK it is!'")
def test_confirm_popup_ok(browser):
    wait = WebDriverWait(browser, 5)
    browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Confirm Popup'"):
        confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirm")))
        confirm_button.click()

    with allure.step("Подтверждаем alert (OK)"):
        alert = wait.until(EC.alert_is_present())
        alert.accept()

    with allure.step("Проверяем текст результата"):
        result = wait.until(EC.presence_of_element_located((By.ID, "confirmResult")))
        assert result.text == "OK it is!"


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Confirm Popup")
@allure.title("Confirm Popup — нажатие кнопки Нет")
@allure.description("При клике на кнопку 'Confirm Popup' появляется диалог с кнопками OK/Cancel. "
                    "Если нажать Cancel — в блоке #confirmResult появляется текст 'Cancel it is!'")
def test_confirm_popup_cancel(browser):
    wait = WebDriverWait(browser, 5)
    browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Confirm Popup'"):
        confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirm")))
        confirm_button.click()

    with allure.step("Отклоняем alert (Cancel)"):
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()

    with allure.step("Проверяем текст результата"):
        result = wait.until(EC.presence_of_element_located((By.ID, "confirmResult")))
        assert result.text == "Cancel it is!"


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Prompt Popup")
@allure.title("Prompt Popup — нажатие Продолжить без ввода текста")
@allure.description("При клике на 'Prompt Popup' и подтверждении без текста "
                    "в #promptResult должен появиться текст 'Fine, be that way...'")
def test_prompt_popup_ok_empty(browser):
    wait = WebDriverWait(browser, 5)
    browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Prompt Popup'"):
        prompt_button = wait.until(EC.element_to_be_clickable((By.ID, "prompt")))
        prompt_button.click()

    with allure.step("Подтверждаем prompt (OK) без текста"):
        alert = wait.until(EC.alert_is_present())
        # просто нажимаем OK, ничего не вводя
        alert.accept()

    with allure.step("Проверяем результат"):
        result = wait.until(EC.presence_of_element_located((By.ID, "promptResult")))
        assert result.text == "Fine, be that way..."


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Prompt Popup")
@allure.title("Prompt Popup — нажатие Отмена")
@allure.description("При клике на 'Prompt Popup' и нажатии Cancel "
                    "в #promptResult должен появиться текст 'Fine, be that way...'")
def test_prompt_popup_cancel(browser):
    wait = WebDriverWait(browser, 5)
    browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Prompt Popup'"):
        prompt_button = wait.until(EC.element_to_be_clickable((By.ID, "prompt")))
        prompt_button.click()

    with allure.step("Отменяем prompt (Cancel)"):
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()

    with allure.step("Проверяем результат"):
        result = wait.until(EC.presence_of_element_located((By.ID, "promptResult")))
        assert result.text == "Fine, be that way..."


@allure.epic("Practice Automation Demo")
@allure.feature("Popups")
@allure.story("Prompt Popup")
@allure.title("Prompt Popup — ввод текста и нажатие Продолжить")
@allure.description("При клике на 'Prompt Popup', вводе текста и подтверждении "
                    "в #promptResult должен появиться текст 'Nice to meet you, <введённый текст>!'")
def test_prompt_popup_ok_with_input(browser):
    wait = WebDriverWait(browser, 5)
    browser.get(BASE_URL)

    with allure.step("Кликаем по кнопке 'Prompt Popup'"):
        prompt_button = wait.until(EC.element_to_be_clickable((By.ID, "prompt")))
        prompt_button.click()

    input_text = "123"

    with allure.step(f"Вводим '{input_text}' в prompt и подтверждаем"):
        alert = wait.until(EC.alert_is_present())
        alert.send_keys(input_text)
        alert.accept()

    with allure.step("Проверяем результат"):
        result = wait.until(EC.presence_of_element_located((By.ID, "promptResult")))
        assert result.text == f"Nice to meet you, {input_text}!"