from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)

all_posts = []
total_pages = 5

for page in range(1, total_pages + 1):
    search_url = f"https://pantip.com/search?q=รถตู้หมอชิต&page={page}"
    driver.get(search_url)
    time.sleep(5)

    threads = driver.find_elements(By.CSS_SELECTOR, "a.link_topic")
    thread_links = [t.get_attribute("href") for t in threads]

    for link in thread_links:
        driver.get(link)
        time.sleep(3)

        posts = driver.find_elements(By.CSS_SELECTOR, "div.display-post-story")
        authors = driver.find_elements(By.CSS_SELECTOR, "a.display-name")
        times = driver.find_elements(By.CSS_SELECTOR, "span.post-meta-inline")

        for post, author, t in zip(posts, authors, times):
            all_posts.append({
                "author": author.text,
                "time": t.text,
                "content": post.text,
                "link": link
            })

df = pd.DataFrame(all_posts)

# Save CSV and JSON in data_csv folder
save_path_csv = os.path.join("..", "data_csv", "pantip_mochit_reviews.csv")
save_path_json = os.path.join("..", "data_csv", "pantip_mochit_reviews.json")

df.to_csv(save_path_csv, index=False, encoding="utf-8")
df.to_json(save_path_json, orient="records", force_ascii=False)

driver.quit()
print(f"Saved {len(all_posts)} posts to CSV and JSON")
