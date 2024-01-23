import json
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from init_driver import init_driver

# Initialize logging
logging.basicConfig(filename='../../logs/scraper.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def create_augment_mapping(driver):
    augment_names = {}
    logging.info("Starting to create augment mapping...")
    for tier in range(1, 4):
        url = f"https://lolchess.gg/guide/augments/set10?tier={tier}&hl=en"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-rbtdul.ept36rh2")))
        augment_containers = driver.find_elements(By.CSS_SELECTOR, "div.css-rbtdul.ept36rh2")

        for container in augment_containers:
            try:
                img_element = container.find_element(By.CSS_SELECTOR, "img")
                img_src = img_element.get_attribute('src')
                if img_src.startswith('//'):
                    img_src = 'https:' + img_src
                augment_name_element = container.find_element(By.CSS_SELECTOR, "div.css-1g520q7 span")
                augment_name = augment_name_element.text.strip()
                augment_names[img_src] = augment_name
            except Exception as e:
                logging.error(f"Error mapping augment: {e}")
    logging.info("Augment mapping creation finished.")
    return augment_names

def save_augment_mapping(augment_mapping, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(augment_mapping, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    driver = init_driver()
    augment_mapping = create_augment_mapping(driver)
    save_augment_mapping(augment_mapping, '../../data/json/augment_mapping.json')
    logging.info("Augment mapping data saved.")
    driver.quit()
