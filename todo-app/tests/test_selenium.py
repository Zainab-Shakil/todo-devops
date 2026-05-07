import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
APP_URL = 'http://todo-container:5000'  # Docker service name
 
@pytest.fixture(scope='module')
def driver():
    """Set up headless Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()
 
 
class TestToDoApp:
 
    def test_page_title(self, driver):
        """
        Test Case 1: Verify the application home page loads
        and has the correct title.
        """
        driver.get(APP_URL)
        time.sleep(2)  # Allow page to fully load
 
        # Assert that the page title contains the expected text
        assert 'To-Do' in driver.title, \
            f'Expected "To-Do" in title, got: {driver.title}'
 
        # Also verify the heading is present
        heading = driver.find_element(By.TAG_NAME, 'h1')
        assert heading is not None, 'Page heading not found'
        print(f'[PASS] Test 1: Page title is "{driver.title}"')
 
 
    def test_add_new_task(self, driver):
        """
        Test Case 2: Verify that a new task can be added
        and appears in the task list.
        """
        driver.get(APP_URL)
        time.sleep(2)
 
        # Define unique test task name
        test_task = 'Automated Test Task 12345'
 
        # Find the input field and enter the task
        task_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'task'))
        )
        task_input.clear()
        task_input.send_keys(test_task)
 
        # Submit the form
        submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
        submit_btn.click()
        time.sleep(2)
 
        # Verify the task appears in the task list
        page_source = driver.page_source
        assert test_task in page_source, \
            f'Expected task "{test_task}" not found in page after submission'
        print(f'[PASS] Test 2: Task "{test_task}" successfully added and visible')
