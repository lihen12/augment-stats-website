import json
import logging
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up logging
logging.basicConfig(filename='../../logs/scraper.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = webdriver.chrome.service.Service('C:\\Program Files\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_top_players(driver, url):
    logging.info("Fetching top players from the leaderboard...")
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody.css-1k9ek97.e1a1fqys2"))
        )
        logging.info("Leaderboard loaded.")
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.css-1k9ek97.e1a1fqys2 > tr.table-row")
        
        players_data = []
        for row in rows[:100]:
            player_name = row.find_element(By.CSS_SELECTOR, "td.summoner a span").text
            profile_link = row.find_element(By.CSS_SELECTOR, "td.summoner a").get_attribute('href')
            players_data.append({"name": player_name, "profile_link": profile_link})
        return players_data
    except Exception as e:
        logging.error(f"An error occurred while fetching top players: {e}")
"""
def create_augment_mapping(driver):
    augment_names = {}
    logging.info("Starting to create augment mapping...")
    for tier in range(1, 4):
        url = f"https://lolchess.gg/guide/augments/set10?tier={tier}&hl=en"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-xr49db")))
        augment_containers = driver.find_elements(By.CSS_SELECTOR, "div.css-rbtdul.ept36rh2")
        
        for container in augment_containers:
            try:
                img_element = container.find_element(By.XPATH, ".//img[starts-with(@src, '//cdn.lolchess.gg')]")
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
"""

def create_augment_mapping(driver):
    augment_names = {}
    logging.info("Starting to create augment mapping...")
    for tier in range(1, 4):
        url = f"https://lolchess.gg/guide/augments/set10?tier={tier}&hl=en"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-rbtdul.ept36rh2")))
        augment_containers = driver.find_elements(By.CSS_SELECTOR, "div.css-xr49db.ept36rh3 div.css-rbtdul.ept36rh2")
        
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


"""
def scrape_player_matches(driver, player_url, augment_mapping):
    all_matches_data = []
    for i in range(1, 6):
        driver.get(f"{player_url}&page={i}")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1mcf40d")))
        matches = driver.find_elements(By.CSS_SELECTOR, "div.css-1mcf40d")
        for match in matches:
            placement = int(match.find_element(By.CSS_SELECTOR, "h5.placement").text.strip('#'))
            augment_images = match.find_elements(By.CSS_SELECTOR, "div.Augments div.item img")

            augments = {label: '' for label in ['2-1', '3-2', '4-2']}
            for index, img in enumerate(augment_images):
                label = ['2-1', '3-2', '4-2'][index]
                augments[label] = augment_mapping.get(img.get_attribute('src'), 'Unknown Augment')

            # Generate a unique identifier for the match
            match_details = f"{player_url}-{placement}-{json.dumps(augments)}"
            match_hash = hashlib.md5(match_details.encode()).hexdigest()

            all_matches_data.append({'unique_id': match_hash, 'placement': placement, 'augments': augments})

    return all_matches_data
"""

def scrape_player_matches(driver, player_url, augment_mapping):
    all_matches_data = []
    for i in range(1, 6):
        driver.get(f"{player_url}&page={i}")
        try:
            # Updated selector for match divs
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-15iyh4v.e1aduscp0")))
            matches = driver.find_elements(By.CSS_SELECTOR, "div.css-15iyh4v.e1aduscp0")
            
            for match in matches:
                placement = int(match.find_element(By.CSS_SELECTOR, "h5.placement").text.strip('#'))
                augment_images = match.find_elements(By.CSS_SELECTOR, "div.Augments div.item img")

                augments = {label: '' for label in ['2-1', '3-2', '4-2']}
                for index, img in enumerate(augment_images):
                    label = ['2-1', '3-2', '4-2'][index]
                    augments[label] = augment_mapping.get(img.get_attribute('src'), 'Unknown Augment')

                # Generate a unique identifier for the match
                match_details = f"{player_url}-{placement}-{json.dumps(augments)}"
                match_hash = hashlib.md5(match_details.encode()).hexdigest()

                all_matches_data.append({'unique_id': match_hash, 'placement': placement, 'augments': augments})

        except TimeoutException:
            print(f"Timeout while trying to load matches for page {i}")

    return all_matches_data
if __name__ == "__main__":
    driver = init_driver()
    players_data = get_top_players(driver, 'https://lolchess.gg/leaderboards?region=global&mode=ranked')
    augment_mapping = create_augment_mapping(driver)
    for player in players_data:
        player_url = player['profile_link'] + '/set10/matches?gameMode=rank'
        matches_data = scrape_player_matches(driver, player_url, augment_mapping)
        filename = f"../../data/json/{player['name'].replace(' ', '_')}_matches_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(matches_data, f, ensure_ascii=False, indent=4)
    logging.info("Data collection complete.")
    driver.quit()
