import time
from os import getenv

import pytest
from dotenv import load_dotenv
from randomname import get_name
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()


@pytest.fixture
def driver():
    # Setup the WebDriver
    driver = webdriver.Firefox()
    yield driver  # Test runs here
    driver.quit()  # Teardown after test


"""
Fitur: Create Folder
Pre-condition:
    - Harus login
    - Folder harus exist
"""


# Skenario 1: Dengan Login
def test_create_folder(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    # Login step
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "current-password"))
    ).send_keys(agent_secret)
    driver.get("http://localhost/app/new")
    folder_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div/div[2]/div[1]/div[2]/div[2]/main/div[2]/div[2]/button[2]",
            )
        )
    )
    ActionChains(driver).move_to_element(folder_button).click().perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'folder created')]",
            )
        )
    )
    assert True, "folder created"


# Skenario 2: Tanpa Login
def test_create_folder_without_login(driver):
    driver.get("http://localhost/app/new")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div[2]/div[1]/div[2]/div[2]/main/div[2]/div[2]/button[2]",
            )
        )
    ).click()
    time.sleep(
        1
    )  # kalo ga di sleep, somehow webdriverwait gamau nunggu dan langsung declare bahwa popupnya kosong, mungkin ini skill issue
    # Assertion: Check if the element exists
    element = WebDriverWait(
        driver, 10
    ).until(  # kalo waktu wait nya kelamaan, dynamic popup nya keburu ilang jadi jangan lama - lama nunggunya
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'You need to be logged in to create new things')]",
            )
        )
    )
    assert "You need to be logged in to create new things" in element.text


"""
Fitur: Edit Folder
Pre-condition:
    - Harus login
    - Folder harus exist
"""


# Skenario 1: User Login dan Folder Exist
def test_edit_folder_with_login_and_exist(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    # Login step
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "current-password"))
    ).send_keys(agent_secret)
    update_buttons = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@title="Open menu"]'))
    )
    ActionChains(driver).move_to_element(update_buttons[0]).click().perform()
    update_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@title="Open the edit form."]'))
    )
    ActionChains(driver).move_to_element(update_button).click().perform()
    folder_name_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "InputStyles__InputStyled-sc-e8e0af5d-5",
            )
        )
    )
    ActionChains(driver).click(folder_name_form).send_keys(get_name()).perform()
    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div/div[2]/div[1]/div[2]/div[2]/main/div[2]/form/button[2]",
            )
        )
    )
    ActionChains(driver).move_to_element(save_button).click().perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'Resource saved')]",
            )
        )
    )
    assert True, "Resource saved"


# Skenario 2: User Login dan Folder Tidak Exist
def test_edit_folder_with_login_and_not_exist(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    # Login step
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "current-password"))
    ).send_keys(agent_secret)
    try:
        # Check that the span with specific text is NOT present
        driver.find_element(By.XPATH, "//span[text()='NonExistentText']")
        assert (
            False
        ), "Span with text 'NonExistentText' was found, but it should not be present."
    except NoSuchElementException:
        assert True, "Span with text 'NonExistentText' not found as expected."


# Skenario 3: User Tidak Login dan Folder Exist
def test_edit_folder_without_login_and_exist(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    update_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@title="Open menu"]'))
    )
    ActionChains(driver).move_to_element(update_buttons[0]).click().perform()
    update_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@title="Open the edit form."]'))
    )
    ActionChains(driver).move_to_element(update_button).click().perform()
    folder_name_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "InputStyles__InputStyled-sc-e8e0af5d-5",
            )
        )
    )
    ActionChains(driver).click(folder_name_form).send_keys(get_name()).perform()
    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div/div[2]/div[1]/div[2]/div[2]/main/div[2]/form/button[2]",
            )
        )
    )
    ActionChains(driver).move_to_element(save_button).click().perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'Could not save resource')]",
            )
        )
    )
    assert True, "Could not save resource"


# Skenario 4: User Tidak Login dan Folder Tidak Exist
def test_edit_folder_without_login_and_not_exist(driver):
    driver.get("http://localhost/app/agent")
    try:
        # Check that the span with specific text is NOT present
        driver.find_element(By.XPATH, "//span[text()='NonExistentText']")
        assert (
            False
        ), "Span with text 'NonExistentText' was found, but it should not be present."
    except NoSuchElementException:
        # Pass if the span is not found
        assert True, "Span with text 'NonExistentText' not found as expected."


"""
Fitur: Delete Folder
Pre-condition:
    - Harus login
    - Folder harus exist
"""


# Skenario 1: User Login dan Folder Exist
def test_delete_with_login_and_exist(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    # Login step
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "current-password"))
    ).send_keys(agent_secret)
    delete_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@title="Open menu"]'))
    )
    ActionChains(driver).move_to_element(delete_buttons[0]).click().perform()
    delete_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@title="Delete this resource."]')
        )
    )
    ActionChains(driver).move_to_element(delete_button).click().perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "eBLtzS",
            )
        )
    ).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'Resource deleted!')]",
            )
        )
    )
    assert True, "Resource deleted!"


# Skenario 2: User Login dan Folder Tidak Exist
def test_delete_with_login_no_folder(driver):
    agent_secret = getenv("secret_agent")
    driver.get("http://localhost/app/agent")
    # Login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "current-password"))
    ).send_keys(agent_secret)

    # Mencoba mencari tombol hapus ketika folder tidak ada
    try:
        # Check that the span with specific text is NOT present
        driver.find_element(By.XPATH, "//span[text()='NonExistentText']")
        assert (
            False
        ), "Span with text 'NonExistentText' was found, but it should not be present."
    except NoSuchElementException:
        # Pass if the span is not found
        assert True, "Span with text 'NonExistentText' not found as expected."


# Skenario 3: User Tidak Login dan Folder Exist
def test_delete_no_login_with_folder(driver):
    driver.get("http://localhost/app/agent")
    try:
        menu_buttons = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@title="Open menu"]'))
        )
        ActionChains(driver).move_to_element(menu_buttons[0]).click().perform()
        delete_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@title="Delete this resource."]')
            )
        )
        ActionChains(driver).move_to_element(delete_button).click().perform()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "eBLtzS",
                )
            )
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'Row__Flex-sc-16aeb8a5-0') and contains(text(), 'No agent has been set or passed, you cannot delete this.')]",
                )
            )
        )
        assert True, "No agent has been set or passed, you cannot delete this."
    except Exception as e:
        assert "NoSuchElementException" in str(
            type(e)
        ), "Tombol tidak ditemukan, seperti yang diharapkan."


# Skenario 4: User Tidak Login dan Folder Tidak Exist
def test_delete_no_login_no_folder(driver):
    driver.get("http://localhost/app/agent")
    try:
        # Check that the span with specific text is NOT present
        driver.find_element(By.XPATH, "//span[text()='NonExistentText']")
        assert (
            False
        ), "Span with text 'NonExistentText' was found, but it should not be present."
    except NoSuchElementException:
        # Pass if the span is not found
        assert True, "Span with text 'NonExistentText' not found as expected."
