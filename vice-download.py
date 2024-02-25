import requests
import sys
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

CONTRIBUTOR = "".join(sys.argv[1:])
LINKS_CLASS = "vice-card-hed__link"
PAGES_CLASS = "pagination_pager__progress-last-page"
CONTENT_CLASS = "article__body-components"
TITLE_CLASS = "smart-header__hed"
DATE_CLASS = "article__header__datebar__date--original"

# Find links to all articles
author_page = "https://www.vice.com/it/contributor/" + CONTRIBUTOR

# Save list of all articles in a text file
def save_articles_list():
    response = requests.get(author_page)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_= LINKS_CLASS, href=True)
    pages = soup.find("span", class_= PAGES_CLASS).get_text()

    author_articles = []
    for page in range(1, int(pages) + 1):
        for link in links:
            author_articles.append("https://www.vice.com" + link["href"])

    print("There are " + str(len(author_articles)) + " articles in memory")

    with open("articoli.txt", "w") as file:
        file.write("\n".join(map(str, author_articles)))

    print("List of all articles saved in file 'articoli.txt'")

def html_to_markdown(title, date, article):
    md_filename = url.split("/")[-1] + ".md"
    markdown_content = md(str(title) + str(date) + "<hr>" + str(article))
    folder_name = "articles/"
    if not os.path.exists(folder_name): 
        os.makedirs(folder_name)
    
    output_path = folder_name + md_filename

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(markdown_content)

save_articles_list()

# Leggi l'elenco delle pagine web remote dal file TXT
with open("articoli.txt", "r") as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()  # Rimuovi spazi e newline
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_title = soup.find("h1")
    article_date = soup.find("div", class_= DATE_CLASS)
    print("Saving article: " + article_title.get_text())
    article_html = soup.find("div", class_= CONTENT_CLASS)
    html_to_markdown(article_title, article_date, article_html)
