import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from credentials import username, password


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chrome_options.add_argument('--start-maximized')
    return chrome_options


@pytest.fixture(autouse=True)
def login(driver):
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(username)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
