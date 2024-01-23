import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from init_driver import init_driver

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
        return []

def save_players_data(players_data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(players_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    url = 'https://lolchess.gg/leaderboards?region=global&mode=ranked'
    driver = init_driver()
    players_data = get_top_players(driver, url)
    save_players_data(players_data, '../../data/json/top_players.json')
    logging.info("Top players data saved.")
    driver.quit()
