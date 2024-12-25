from curl_cffi import requests
from bs4 import BeautifulSoup
from data import Data
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()


def get_job():

    options = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "cookie": f"{os.getenv('COOKIE')}",
    }

    req = requests.get(
        "https://www.upwork.com/nx/search/jobs/?nbs=1&q=web%20scraping",
        impersonate="chrome",
        headers=options,
    ).text

    soup = BeautifulSoup(req, "html.parser")

    jobs = soup.findAll("article", class_=["job-title", "cursor-pointer"])

    file_json = "jobs.json"

    if os.path.exists(file_json):
        with open(file_json, "r", encoding="utf-8") as file:
            data_awal = json.load(file)
    else:
        data_awal = []

    existing_links = {item["link"] for item in data_awal}

    for job in jobs:
        judul = job.find("h2", class_="job-tile-title").text
        link = job.find("a", class_="up-n-link").get("href")

        dict_item = {"judul": judul, "link": link}

        if link not in existing_links:
            data_awal.append(dict_item)
            existing_links.add(link)
            print("Job baru:", judul)

            send_wa(judul, link)

    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(data_awal, file, indent=4, ensure_ascii=False)
    print("mencari")


def send_wa(nama_job, link_job):

    url = "https://api.fonnte.com/send"

    data = {
        "target": f"{os.getenv('NO_HP')}",
        "message": f"job baru {nama_job} \n \n https://www.upwork.com{link_job}",
        "schedule": 0,
        "typing": False,
        "delay": "2",
        "countryCode": "62",
        "followup": 0,
    }
    headers = {"Authorization": f"{os.getenv('KODE_FONNTE')}"}
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            print("Response:", response.text)
        else:
            print(f"Failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":

    while True:
        get_job()
        time.sleep(60)
