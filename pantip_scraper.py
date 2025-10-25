import requests
from bs4 import BeautifulSoup
import configparser
import time

num_pages = 5
base_url = "https://pantip.com/forum/motor"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

reviews = []

for page in range(1, num_pages + 1):
    url = f"{base_url}?page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    threads = soup.select("div.sc-1njr3zj-0")  # ปรับ selector ตาม Pantip ล่าสุด
    
    for t in threads:
        title_tag = t.select_one("a")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link = "https://pantip.com" + title_tag["href"]
        
        thread_res = requests.get(link, headers=headers)
        thread_soup = BeautifulSoup(thread_res.text, "html.parser")
        content_tag = thread_soup.select_one("div.sc-1v1d5rx-0")
        content = content_tag.text.strip() if content_tag else ""
        
        author_tag = thread_soup.select_one("a.sc-1rp9nay-1")
        author = author_tag.text.strip() if author_tag else ""
        
        date_tag = thread_soup.select_one("time")
        date = date_tag.text.strip() if date_tag else ""
        
        reviews.append({"หัวข้อ": title, "ผู้โพสต์": author, "วันที่": date, "ข้อความรีวิว": content})
        time.sleep(1)

config = configparser.ConfigParser()
for i, review in enumerate(reviews, start=1):
    section = f"รีวิว{i}"
    config[section] = review

with open("reviews.ini", "w", encoding="utf-8") as configfile:
    config.write(configfile)

print("เสร็จเรียบร้อย! สร้างไฟล์ reviews.ini แล้ว")
