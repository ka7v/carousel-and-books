import requests
from bs4 import BeautifulSoup
import multiprocessing
from book.konstants import *
from book.model import Books, Genres, User, Auther, Language
from book import db
from book.download_image import dow_img



class parser:
    def __init__(self, url, parser_type=PARESER_TYPE):
        response = requests.get(url=url)
        content = response.content
        self.soup = BeautifulSoup(content, parser_type)

    def parse(self):
        title = self.soup.find('div', class_="product--box box--basic").find('a', class_="product--title").get_text(strip=True)
        print(title)
        date = self.soup.find('div', class_="product--box box--basic").find_all('span', class_="grq--book-entry-name")
        print(date)
        image = self.soup.find('div', class_="image--element").get("style").replace('background-image: url(','').replace(');', '').replace("'", "")
        print(image)
        about = self.soup.find('div', class_="product--description").get_text(strip=True)
        print(about)
        result = {
            'ganre': date[2].get_text().split()[0],
            'name': title,
            'author': date[0].get_text(strip=True),
            'about_book': about,
            'langueges': date[4].get_text(strip=True),
            'image': image
        }
        return result


def get_url(url):
    book_list = []
    try:
        a = parser(url=url)
        book_list.append(a.parse())
        # for i in book_list:
        #     if i['image']:
        #         im = dow_img(url=i['image'], filename=i['name'])
        #     else:
        #         im = 'images/standart.jpg'
        #     book = Books(name=i['name'], description=i['about_book'], photo=f'{im}')
        #     db.session.add(book)
        #     db.session.commit()
        #     book_genre = Genres(genre=i['ganre'], book_id=book.id)
        #     db.session.add(book_genre)
        #     db.session.commit()
        #     book_auther = Auther(name=i['author'], book_id=book.id)
        #     db.session.add(book_auther)
        #     db.session.commit()
        #     book_language = Language(language=i['langueges'], book_id=book.id)
        #     db.session.add(book_language)
        #     db.session.commit()
    except Exception as e:
        pass
    return book_list

link_ls = []
for i in range(HREF3, HREF4):
    link_ls.append((f'https://books.am/am/catalog/product/view/id/{i}/category/7464/'))
if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        print(p.map(get_url, link_ls))

