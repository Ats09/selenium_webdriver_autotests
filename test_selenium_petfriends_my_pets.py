import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Проверка отсутствия одинаковых питомцев
def test_no_duplicate_pets(driver):
    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    pet_rows = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr')

    # Проверка, что найдены строки с питомцами
    assert len(pet_rows) > 0, "Строки с питомцами не найдены"

    pet_identifiers = set()
    repeated_pets = []

    for row in pet_rows:
        # Получаем текст ячеек строки
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) == 4:
            name = cells[0].text.strip()
            breed = cells[1].text.strip()
            age = cells[2].text.strip()
            pet_identifier = f"{name}:{breed}:{age}"

            if pet_identifier in pet_identifiers:
                repeated_pets.append(pet_identifier)
            else:
                pet_identifiers.add(pet_identifier)

    # Проверяем, что нет повторяющихся питомцев
    assert not repeated_pets, f"Найдены повторяющиеся питомцы: {repeated_pets}"
    print("\nНету повторяющихся питомцев.")


# Проверка совпадения количества питомцев в профиле пользователя с таблицей
def test_check_user_profile(driver):

    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
    user_info_elements = driver.find_elements(By.XPATH, '//div[@class=".col-sm-4 left"]')
    pet_count_number = 0

    # Явное ожидание, что найдены элементы с информацией о пользователях
    user_info_elements_present = EC.presence_of_all_elements_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))
    WebDriverWait(driver, 10).until(user_info_elements_present)

    for element in user_info_elements:
        # Получаем текст элемента
        element_text = element.text

        # Проверка, что текст элемента не пустой
        assert element_text != "", "Текст элемента пустой"

        # Используем регулярное выражение для извлечения числа из строки
        pet_count = re.search(r'Питомцев:\s*(\d+)', element_text)

        if pet_count:
            pet_count_number = int(pet_count.group(1))

    # Явное ожидание, что найдены элементы с именами питомцев
    names_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#all_my_pets .table tbody tr'))
    WebDriverWait(driver, 10).until(names_present)

    print("\nКоличество питомцев в профиле пользователя: ", pet_count_number)
    print("\nКоличество питомцев в таблице: ", len(names))
    # Проверяем, что число питомцев в таблице и профиле совпадают
    assert pet_count_number == len(names)
    print("\nКоличества питомцев в таблице и профиле пользователя совпадают.")


# Проверка, что у всех питомцев есть имя, возраст и порода.
def test_check_animal_data(driver):
    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets .table tbody tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    pet_rows = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')

    for i in range(len(pet_rows)):
        # Явное ожидание, что найдена строка с информацией о питомце
        pet_row_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'#all_my_pets .table tbody tr:nth-child({i + 1})'))
        WebDriverWait(driver, 10).until(pet_row_present)

        # Получаем информацию о питомце
        parts = pet_rows[i].text.split(' ')

        if len(parts) == 3:
            print('\nИмя, порода и возраст: ', pet_rows[i].text.split(' '))
        else:
            print('Есть пустые поля')

    print('У всех питомцев есть имя, возраст и порода.')


# Проверка, что у всех питомцев разные имена
def test_check_animal_name(driver):

    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets .table tbody tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    pet_rows = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')

    pet_names = []
    repeated_pet_names = []

    for i in range(len(pet_rows)):

        # Явное ожидание, что найдена строка с информацией о питомце
        pet_row_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'#all_my_pets .table tbody tr:nth-child({i + 1})'))
        WebDriverWait(driver, 10).until(pet_row_present)

        # Получаем информацию о питомце
        pet_row = pet_rows[i].text
        pet_names.append(pet_row)

    if pet_names.count(pet_rows) > 1 and pet_rows not in repeated_pet_names:
        repeated_pet_names.append(pet_rows)

    # Проверяем, что нет повторяющихся имен питомцев
    assert not repeated_pet_names
    print("\nУ всех питомцев разные имена.")


# Проверка, что у половины питомцев есть фото
def test_check_number_pets_with_photo(driver):

    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets .table tbody tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    pet_rows = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
    images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr th[scope="row"] img')
    pets_with_photo_count = 0

    for i in range(len(pet_rows)):

        # Явное ожидание, что найдена строка с информацией о питомце
        pet_row_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'#all_my_pets .table tbody tr:nth-child({i + 1})'))
        WebDriverWait(driver, 10).until(pet_row_present)

        pet_row = pet_rows[i]
        pet_name = pet_row.find_element(By.TAG_NAME, 'td').text.strip()
        pet_image = images[i].get_attribute('src')

        if pet_image is not None and pet_image.strip() != '':
            pets_with_photo_count += 1
            print(f"\nУ питомца {pet_name} есть фото.")
        else:
            print(f"\nУ питомца {pet_name} нет фото.")

    assert pets_with_photo_count >= len(pet_rows) / 2

    print(f"\nУ половины питомцев есть фото.\nУ {pets_with_photo_count} из {len(pet_rows)} есть фото.")


# Проверка, что у всех питомцев есть фото
def test_check_pet_photo(driver):

    # Неявное ожидание загрузки страницы с питомцами пользователя
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Явное ожидание загрузки таблицы с питомцами
    table_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets .table tbody tr'))
    WebDriverWait(driver, 10).until(table_loaded)

    pet_rows = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
    images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr th[scope="row"] img')

    for i in range(len(pet_rows)):

        # Явное ожидание, что найдено изображение питомца
        image_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'#all_my_pets .table tbody tr:nth-child({i + 1}) th[scope="row"] img'))
        WebDriverWait(driver, 10).until(image_present)

        image_src = images[i].get_attribute('src')

        # Проверка наличия картинки у питомца
        assert image_src is not None and image_src.strip() != ''

    print("\nУ всех питомцев есть фото.")
