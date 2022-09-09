import requests
from bs4 import BeautifulSoup
import multiprocessing
from book.konstants import *
from book.model import Books, Genres, User, Auther, Language
from book import db
from book.download_image import dow_img


class parser:
    def __init__(self, url, parser_type = PARESER_TYPE ):
        response = requests.get(url=url)
        content = response.content
        self.soup = BeautifulSoup(content, parser_type)

    def parse(self):
        date = self.soup.find('div', class_="product attribute section_title").get_text(strip=True)
        author = self.soup.find('div', class_= "product_brand").get_text(strip=True)
        about = self.soup.find('div', class_="product attribute inner_description").get_text(strip=True)
        page_count = self.soup.find_all('div', class_ = "details_answer")[5].get_text(strip=True)
        languages = self.soup.find_all('div', class_="details_answer")[3].get_text(strip=True)
        if len(languages) < 4:
            languages = 'language -'
            page_count = self.soup.find_all('div', class_="details_answer")[4].get_text(strip=True)
        genre = 'Հայ գրականություն'
        try:
            imagie = self.soup.find('img', class_="image_big_change").get('src')
        except:
            imagie = ''
        result = {
            'ganre': genre,
            'name': date,
            'author': author,
            'about_book': about,
            'langueges': languages,
            'page_count': page_count,
            'image': imagie
        }
        return result

def get_url(url):
    book_list = []
    try:
        a = parser(url=url)
        book_list.append(a.parse())
        try:
            for i in book_list:
                if i['image']:
                    filename = i['name'].replace(' ', '')
                    im = dow_img(url=i['image'], filename=filename)
                    print(im)
                else:
                    im = 'images/standart.jpg'
                book = Books(name=i['name'], description=i['about_book'], photo=f'{im}', page_count=i['page_count'])
                db.session.add(book)
                db.session.commit()
                user = User.query.get(1)
                book.user_book.append(user)
                book_genre = Genres(genre=i['ganre'], book_id=book.id)
                db.session.add(book_genre)
                db.session.commit()
                if i['author']:
                    book_auther = Auther(name=i['author'], book_id=book.id)
                else:
                    book_auther = Auther(name='auther -', book_id=book.id)
                db.session.add(book_auther)
                db.session.commit()
                book_language = Language(language=i['langueges'], book_id=book.id)
                db.session.add(book_language)
                db.session.commit()
        except Exception as ex:
            print(ex)
    except Exception as e:
        pass
    return book_list


link_ls = []
for i in range(HREF1, HREF2):
    # a = 'https://books.am/am/catalog/product/view/id/5905/category/7464/'
    link_ls.append((f'https://books.am/am/catalog/product/view/id/{i}/category/7472/'))
if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        print(p.map(get_url, link_ls))