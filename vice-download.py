import requests
import sys
from bs4 import BeautifulSoup
from markdownify import markdownify as md

CONTRIBUTOR = "".join(sys.argv[1:])

# Find links to all articles
author_page = "https://www.vice.com/it/contributor/" + CONTRIBUTOR

# Save list of all articles in a text file
def save_articles_list():
    response = requests.get(author_page)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="vice-card-hed__link", href=True)
    pages = soup.find("span", class_="pagination_pager__progress-last-page").get_text()

    author_articles = []
    for page in range(1, int(pages) + 1):
        for link in links:
            author_articles.append("https://www.vice.com" + link["href"])

    print("There are " + str(len(author_articles)) + " articles in memory")

    with open("articoli.txt", "w") as file:
        file.write("\n".join(map(str, author_articles)))

    print("List of all articles saved in file 'articoli.txt'")

save_articles_list()
