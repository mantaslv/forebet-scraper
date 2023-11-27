from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from tqdm import tqdm
import json
import time
import re

def save_page_source(driver, filename='page_source.html'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

def find_el(location, value, multiple=False):
    if multiple: func = location.find_elements
    else: func = location.find_element
    try: return func(by=By.CSS_SELECTOR, value=value)
    except: pass

def convert_odds(odds):
    try:
        odds = odds.split('/')
        return int(odds[0])/int(odds[1]) + 1
    except: return None

def convert_score(score):
    try:
        score = score.strip('()').split(' - ')
        return {'home': int(score[0]), 'away': int(score[1])}
    except: return {'home': None, 'away': None}
    
def selenium_scraper(date):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1200')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    )    
    options.add_argument('--header=Accept-Language: en-US,en;q=0.9')
    driver = webdriver.Chrome(options=options)

    url = 'https://www.forebet.com/en/football-predictions/predictions-1x2/' + date
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.contentmiddle div div.schema")))
    
    try:
        more_rows_button = driver.find_element(by=By.CSS_SELECTOR, value="#mrows span")
        if more_rows_button:
            driver.execute_script("arguments[0].click();", more_rows_button)
            time.sleep(5)
    except: pass

    table = driver.find_element(by=By.CSS_SELECTOR, value="td.contentmiddle div div.schema")
    rows = table.find_elements(by=By.CSS_SELECTOR, value="div.rcnt")

    data = []
    
    for row in tqdm(rows):
        d = dict()
        row.location_once_scrolled_into_view

        d['league'] = find_el(row, ".shortTag").text
        d['team_home'] = find_el(row, ".homeTeam span").text
        d['team_away'] = find_el(row, ".awayTeam span").text
        d['date_time'] = datetime.strptime(find_el(row, ".date_bah").text, '%d/%m/%Y %H:%M').isoformat()
        
        probs = find_el(row, ".fprc span", True)
        d['prob_home'] = int(probs[0].text)
        d['prob_draw'] = int(probs[1].text)
        d['prob_away'] = int(probs[2].text)
        
        exp_score = convert_score(find_el(row, ".ex_sc").text)
        d['exp_score_home'] = exp_score['home']
        d['exp_score_away'] = exp_score['away']
        d['exp_goals'] = float(find_el(row, ".avg_sc").text)
        
        temp_el = find_el(row, ".wnums")
        text = temp_el.text if temp_el else ""
        d['temp'] = int(text[:-1]) if text[:-1] else None

        expand_odds_btn = find_el(row, ".lscrsp")
        driver.execute_script("arguments[0].click();", expand_odds_btn)
        odds_table = find_el(driver, "table.simplodd")
        odds = find_el(odds_table, "span", True)
        d['odds_home'] = convert_odds(odds[0].text)
        d['odds_draw'] = convert_odds(odds[1].text)
        d['odds_away'] = convert_odds(odds[2].text)

        d['status'] = find_el(row, ".scoreLnk").text

        score = convert_score(find_el(row, ".l_scr").text)
        d['score_home'] = score['home']
        d['score_away'] = score['away']

        ht_score_el = find_el(row, ".ht_scr")
        ht_score = ht_score_el.text if ht_score_el else None
        d['ht_score_home'] = convert_score(ht_score)['home']
        d['ht_score_away'] = convert_score(ht_score)['away']

        data.append(d)

    driver.quit()

    with open(f'data/forebet_{date}.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return data

start_date = '2023-11-03'
end_date = '2023-11-25'

start = datetime.strptime(start_date, '%Y-%m-%d')
end = datetime.strptime(end_date, '%Y-%m-%d')

current_date = start
while current_date <= end:
    date_string = current_date.strftime('%Y-%m-%d')
    result = selenium_scraper(date_string)
    current_date += timedelta(days=1)