import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to WebDriver executable
driver_path = 'C:\\Program Files\\chromedriver-win64\\chromedriver.exe'
leaderboard_url = 'https://lolchess.gg/leaderboards?region=global&mode=ranked'

# Function to initialize the WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode, without a UI
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    return driver

# Function to get top 100 players
def get_top_players(driver, url):
    print("Fetching top players from the leaderboard...")
    driver.get(url)
    try:
        # Wait for the leaderboard to load and be visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody.css-1k9ek97.e1a1fqys2"))
        )
        print("Leaderboard loaded.")
        # Find the rows of the leaderboard table within the tbody
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.css-1k9ek97.e1a1fqys2 > tr.table-row")
        print(f"Found {len(rows)} rows in the leaderboard.")
        
        players_data = []
        for row in rows[:100]:  # Limit to top 100 players
            # Extract the player name and profile link
            player_name = row.find_element(By.CSS_SELECTOR, "td.summoner a span").text
            profile_link = row.find_element(By.CSS_SELECTOR, "td.summoner a").get_attribute('href')
            print(f"Player found: {player_name}, Profile link: {profile_link}")
            players_data.append({"name": player_name, "profile_link": profile_link})
        return players_data
    except Exception as e:
        print(f"An error occurred while fetching top players: {e}")

# Function to get player augments
def get_player_augments(driver, player_data):
    print("Fetching player augments...")
    all_players_augments = []
    for player in player_data:
        player_name = player['name']
        profile_url = player['profile_link']
        augment_url = profile_url + '/set9.5/statistics?staticType=augments'
        print(f"Fetching augments for player: {player_name}, URL: {augment_url}")
        driver.get(augment_url)
        try:
            # Wait for the augments to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.css-3d12d6.e18d73ac0"))
            )
            print("Augments page loaded.")
            # Find the augment rows in the table
            augment_rows = driver.find_elements(By.CSS_SELECTOR, "table.css-3d12d6.e18d73ac0 > tbody > tr")
            print(f"Found {len(augment_rows)} augments for player: {player_name}")
            augments_data = []
            for row in augment_rows:
                # Extract the augment data
                name = row.find_element(By.CSS_SELECTOR, "td.name span.name-text").text
                plays = row.find_element(By.CSS_SELECTOR, "td.plays").text
                win_rate = row.find_element(By.CSS_SELECTOR, "td.winRate").text
                top_rate = row.find_element(By.CSS_SELECTOR, "td.topRate").text
                avg_rank = row.find_element(By.CSS_SELECTOR, "td.avgRank").text
                print(f"Augment found: {name}, Plays: {plays}, Win Rate: {win_rate}, Top Rate: {top_rate}, Avg Rank: {avg_rank}")
                augments_data.append({
                    "name": name,
                    "plays": plays,
                    "win_rate": win_rate,
                    "top_rate": top_rate,
                    "avg_rank": avg_rank
                })
            all_players_augments.append({
                "player": player_name,
                "augments": augments_data
            })
        except Exception as e:
            print(f"An error occurred while fetching augments for player {player_name}: {e}")
    return all_players_augments

# Main script execution
if __name__ == "__main__":
    driver = init_driver()  # Initialize the WebDriver
    try:
        # Get the top 100 players from the leaderboard
        top_players_data = get_top_players(driver, leaderboard_url)

        # If top players were found, fetch their augments
        if top_players_data:
            print("Top players data fetched successfully. Fetching augments...")
            top_players_augments = get_player_augments(driver, top_players_data)
            # Save the data to a JSON file
            with open('top_players_augments.json', 'w') as json_file:
                json.dump(top_players_augments, json_file, indent=4)
            print("Top 100 players' augment data has been saved to top_players_augments.json")
        else:
            print("Failed to retrieve top players data.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Quit the driver after all operations are complete
