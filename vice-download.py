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
ARTICLES_FILENAME = "articles.txt"
ARTICLES_FOLDERNAME = "articles/"

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

    with open(ARTICLES_FILENAME, "w") as file:
        file.write("\n".join(map(str, author_articles)))

    print("List of all articles saved in file " + ARTICLES_FILENAME)

def html_to_markdown(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1")
    date = soup.find("div", class_= DATE_CLASS)
    article = soup.find("div", class_= CONTENT_CLASS)
    md_filename = url.split("/")[-1] + ".md"
    markdown_content = md(str(title) + str(date) + "<hr>" + str(article))
    folder_name = ARTICLES_FOLDERNAME

    if not os.path.exists(folder_name): 
        os.makedirs(folder_name)
    
    output_path = folder_name + md_filename

    with open(output_path, "w", encoding="utf-8") as file:
        print("Saving article: " + title.get_text())
        file.write(markdown_content)

save_articles_list()

def save_as_markdown():
    with open(ARTICLES_FILENAME, "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        html_to_markdown(url)

user_input = input("Save all articles as markdown files? (yes/no): ")

if user_input.lower() == "yes":
    save_as_markdown()
