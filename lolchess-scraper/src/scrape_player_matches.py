import json
import logging
import hashlib
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from init_driver import init_driver

# Initialize logging
logging.basicConfig(filename='../../logs/scraper.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_augment_mapping(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Augment mapping file not found: {filepath}")
        return {}

def scrape_player_matches(driver, player_url, augment_mapping):
    all_matches_data = []
    for i in range(1, 6):  # Adjust the range as needed
        try:
            page_url = f"{player_url}&page={i}"
            driver.get(page_url)
            logging.info(f"Accessing page: {page_url}")
            
            match_container_selector = "div.css-15iyh4v.e1aduscp0"
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, match_container_selector)))
            logging.info(f"Match container elements found on page {i}")

            matches = driver.find_elements(By.CSS_SELECTOR, match_container_selector)
            for match in matches:
                try:
                    placement_selector = "h5.placement"
                    placement = int(match.find_element(By.CSS_SELECTOR, placement_selector).text.strip('#'))
                    logging.info(f"Placement found: {placement}")

                    augment_images_selector = "div.Augments div.item img"
                    augment_images = match.find_elements(By.CSS_SELECTOR, augment_images_selector)

                    augments = {label: '' for label in ['2-1', '3-2', '4-2']}
                    for index, img in enumerate(augment_images):
                        label = ['2-1', '3-2', '4-2'][index]
                        augments[label] = augment_mapping.get(img.get_attribute('src'), 'Unknown Augment')
                        logging.info(f"Augment for {label} phase found: {augments[label]}")

                    # Generate a unique identifier for the match
                    match_details = f"{player_url}-{placement}-{json.dumps(augments)}"
                    match_hash = hashlib.md5(match_details.encode()).hexdigest()
                    logging.info(f"Match hash generated: {match_hash}")

                    all_matches_data.append({'unique_id': match_hash, 'placement': placement, 'augments': augments})
                except NoSuchElementException as e:
                    logging.error(f"Element not found in match: {e}")
        except TimeoutException:
            logging.error(f"Timeout while trying to load matches for page {i}")

    return all_matches_data

def save_matches_data(matches_data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(matches_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    player = {
        "name": "Havalı nick#TR1",
        "profile_link": "https://lolchess.gg/profile/tr/Haval%C4%B1%20nick-TR1"
    }
    driver = init_driver()
    augment_mapping = load_augment_mapping('../../data/json/augment_mapping.json')
    player_url = player['profile_link'] + '/set10/matches?gameMode=rank'
    matches_data = scrape_player_matches(driver, player_url, augment_mapping)
    save_matches_data(matches_data, f'../../data/json/{player["name"].replace(" ", "_")}_matches_data.json')
    logging.info(f"Match data for {player['name']} saved.")
    driver.quit()
