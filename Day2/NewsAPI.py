
import requests
import os
import time
import re
import json
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()
API_KEY = os.getenv("news_api_key")

with open("config.json", "r") as cfg:
    cfg_data = json.load(cfg)
CATEGORY_KEYWORDS = cfg_data.get("CATEGORY_KEYWORDS", cfg_data)
TECH_COMPANIES = cfg_data.get("TECH_COMPANIES", [])
FINANCE_COMPANIES = cfg_data.get("FINANCE_COMPANIES", [])

def fetch_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "stock market OR companies OR business",
        "pageSize": 50,
        "apiKey": API_KEY
    }

    for i in range(3):
        try:
            response = requests.get(url, params=params, timeout=10)
        except RequestException:
            return []

        if response.status_code == 200:
            return response.json()["articles"]

        elif response.status_code == 429:
            time.sleep(2 ** i)

    return []

class NewsClassifier:
    def __init__(self, config):
        self.config = config

    def classify(self, text):
        text = text.lower()
        # if not self.config:
        #     return "GENERAL"

        for category in ["FINANCE", "TECH", "POLITICS"]:
            for word in self.config.get(category, []):
                if word.lower() in text:
                    return category
                
        return "GENERAL"

def extract_entities(text, category):
    if category == "TECH":
        companies_list = TECH_COMPANIES
    elif category == "FINANCE":
        companies_list = FINANCE_COMPANIES
    else:
        companies_list = [] 
    companies_found = []
    lowered = text.lower()
    for company in companies_list:
        if not company:
            continue
        if company.lower() in lowered and company not in companies_found:
            companies_found.append(company)

    currency = list(dict.fromkeys(re.findall(r'[\$₹€£]\d+(?:,\d{3})*(?:\.\d+)?', text)))
    percentage = list(dict.fromkeys(re.findall(r'\d+(?:\.\d+)?%', text)))

    return {
        "companies": companies_found,
        "currency": currency,
        "percentage": percentage
    }

def main():
    articles = fetch_news()
    classifier = NewsClassifier(CATEGORY_KEYWORDS)

    output = []

    for article in articles:
        title = article["title"] or ""
        description = article["description"] or ""

        text = title + " " + description

        category = classifier.classify(text)
        entities = extract_entities(text, category)

        output.append({
            "title": title,
            "category": category,
            "entities": entities
        })

    with open("news_data.json", "w") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()
