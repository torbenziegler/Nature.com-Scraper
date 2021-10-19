import os
import string

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.nature.com/nature/articles"


def get_article(url, current_page, search_term):
    request = requests.get(url)
    if request:
        soup = BeautifulSoup(request.content, "html.parser")
        for article in soup.find_all("article"):
            article_type = article.find('span', {'class': "c-meta__type"}).text.strip()
            if article_type == search_term:
                article_href = article.find('a', {'data-track-action': 'view article'})['href']
                article_link = requests.get(f'https://www.nature.com{article_href}')
                article_title = article.find('a').text
                article_title = article_title.translate(str.maketrans('', '', string.punctuation))
                article_title = article_title.translate(str.maketrans(' ', '_'))
                article_soup = BeautifulSoup(article_link.content, "html.parser")
                article_body = article_soup.find('div', {'class': 'c-article-body u-clearfix'})
                with open(f'Page_{current_page}/{article_title}.txt', 'w', encoding='UTF-8') as file:
                    try:
                        file.write(article_body.text)
                        file.close()
                        print("File created: " + article_title)
                    except AttributeError:
                        print("Article can't be accessed.")


def crawl(pages, search_term):
    for page in range(1, pages + 1):
        try:
            os.mkdir(f"Page_{page}")
            print(f"Directory 'Page_{page}' created")
        except FileExistsError:
            print(f"Directory 'Page_{page}' already exists.")

        target_url = f"{BASE_URL}?searchType=journalSearch&sort=PubDate&year=2020&page={page}"
        get_article(target_url, page, search_term)


crawl(int(input("Enter page amount:")), input("Enter article type:"))
