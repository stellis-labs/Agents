import requests
from bs4 import BeautifulSoup
import json
import re
import time

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)  
    text = re.sub(r"\[\d+\]", "", text)  
    return text.strip()


def extract_main_question(soup):
    possible_selectors = [
        "h1",  
        "div.topic-identifier",  
        "div.topic-header h1",  
        "h1.font-serif"  
    ]

    for selector in possible_selectors:
        question_element = soup.select_one(selector)
        if question_element:
            return clean_text(question_element.text)
    
    return None  

def extract_arguments(soup, argument_class, argument_type, start_index):
    arguments = []
    sections = soup.find_all("section", class_=argument_class)
    
    for i, section in enumerate(sections):
        heading = section.find("h2")  
        if not heading:
            continue
        
        perspective_number = start_index + i + 1
        argument_title = f"Perspective {perspective_number}: [{argument_type}] {clean_text(heading.text)}"
        
        
        evidence_paragraphs = section.find_all("p")
        evidence = [clean_text(p.text) for p in evidence_paragraphs if p.text.strip()]

       
        if not evidence:
            continue
        
        arguments.append({
            "argument": argument_title,
            "evidence": evidence
        })
    
    return arguments


def extract_debate_data(article_url):
    print(f"Fetching article: {article_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {article_url}, Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

   
    main_question = extract_main_question(soup)
    if not main_question:
        print(f"Skipping {article_url} - No main question found.")
        return None

    
    arguments = []
    arguments += extract_arguments(soup, "pro", "Pro", len(arguments))
    arguments += extract_arguments(soup, "con", "Con", len(arguments))

    
    if not arguments:
        print(f"Skipping {article_url} - No arguments found.")
        return None

    return {
        "question": main_question,
        "arguments": arguments
    }


def get_article_links(main_url):
    print(f"Fetching main page: {main_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    response = requests.get(main_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {main_url}, Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    
    article_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/procon/" in href and not href.endswith("/procon/"):
            full_url = f"https://www.britannica.com{href}" if href.startswith("/") else href
            article_links.append(full_url)

   
    article_links = list(set(article_links))
    print(f"Found {len(article_links)} articles.")
    
    return article_links


def scrape_procon_articles(main_url):
    article_links = get_article_links(main_url)
    if not article_links:
        print("No articles found. Exiting.")
        return

    debate_data = []
    for index, link in enumerate(article_links):
        print(f"Scraping ({index + 1}/{len(article_links)}): {link}")
        try:
            data = extract_debate_data(link)
            if data:
                debate_data.append(data)
        except Exception as e:
            print(f"Error scraping {link}: {e}")

        time.sleep(1)  

    
    with open("procon_debates.json", "w", encoding="utf-8") as f:
        json.dump(debate_data, f, indent=4, ensure_ascii=False)

    print("Scraping complete. Data saved to 'procon_debates.json'.")


if __name__ == "__main__":
    main_url = "https://www.britannica.com/procon"
    scrape_procon_articles(main_url)
