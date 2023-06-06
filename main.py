import requests
import string
import os
from bs4 import BeautifulSoup


def main():
    pages = int(input())
    articles_type = input()

    while pages:
        url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={pages}'
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(response.content, 'html.parser')

        if response.status_code == 200:
            articles_list = []
            find_all_articles(articles_list, soup, articles_type)
            titles = []
            os.mkdir(f'Page_{pages}')
            for x in articles_list:
                title = format_title(titles, x)
                create_file(title, x, pages)
        else:
            print(f'\nThe URL returned {response.status_code}!')
        pages = pages - 1
    print("Saved all articles.")


def format_title(titles, x):
    title = x.text
    title = title.strip()
    title = title.strip(string.punctuation)
    title = title.replace(' ', '_')
    titles.append(title + '.txt')
    return title


def create_file(title, x, pages):
    file = open(f'{os.getcwd()}/Page_{pages}/{title}.txt', 'wb')
    link = x.get('href')
    link_response = requests.get(f'https://www.nature.com{link}', headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(link_response.content, 'html.parser')
    file.write(soup.find('p', {'class': 'article__teaser'}).text.encode('UTF-8'))
    file.close()


def find_all_articles(articles_list, soup, articles_type):
    articles = soup.findAll('span', {'class': 'c-meta__item c-meta__item--block-at-lg'}, text=articles_type)
    for article in articles:
        anchor = article.find_parent('article').find('a', {'data-track-action': 'view article'})
        if anchor:
            articles_list.append(anchor)


if __name__ == '__main__':
    main()
