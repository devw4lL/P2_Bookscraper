import requests

from bs4 import BeautifulSoup
from pprint import pprint


class HtmlParser:
    def __init__(self, product_url):
        self.product_page_url = product_url
        self.universal_product_code = ""
        self.title = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.number_available = 0
        self.product_description = ""
        self.category = ""
        self.review_rating = 0
        self.image_url = ""

    def get_response(self):
        """Fait une requete GET sur une URL, vérifie ca validité et
         stock son code html dans un variable.

         Args:
            self.product_page_url (str): URL a analyser.

        :return:
            requests.models.response(obj): Contient le code HTML de l'URL dans un objet requests.
        """
        try:
            self.response = requests.get(self.product_page_url)
            if self.response.ok:
                return self.response
        except requests.exceptions.RequestException as e:
            print(f"ERREUR sur get_reponse: {e}")
            return False

    def get_all_category(self):
        """Extraire les URLs de chaque catégorie.

            Args:
                requests.models.response(obj): Contient le code HTML de l'URL dans un objet requests.

        :return:
            list: List d'URLs de chaque catégorie.
        """
        all_categorys_urls = []

        try:
            soup = BeautifulSoup(self.response.text, 'lxml')
            raw_category = soup.find("ul", class_="nav nav-list").li
            for raw in raw_category.findAll("a"):
                all_categorys_urls.append(f"{self.product_page_url}{raw['href']}")
            return all_categorys_urls[1:]

        except Exception as e:
            print(f"ERREUR sur get_all_category: {e}")
            return False

    def extract_products_urls(self):
        """Extraire les URLs de chaque produits.

            Args:
                requests.models.response(obj): Contient le code HTML de l'URL dans un objet requests.

        :return:
            list: list d'URLs de chaque produit.
        """
        all_products_urls = []
        next_ = True
        try:
            soup = BeautifulSoup(self.response.text, "lxml")
            while next_:
                raw_url = soup.findAll("div", class_="image_container")
                for url in raw_url:
                    all_products_urls.append("/".join(self.product_page_url.split('/')[:4])
                                             + "/"
                                             + "/".join(url.find("a")['href'].split("/")[3:]))
                next_p = soup.find("li", class_="next")
                if next_p:
                    next_page = self.product_page_url.replace("index.html", next_p.find("a")['href'])
                    self.product_page_url = next_page
                    self.get_response()
                    soup = BeautifulSoup(self.response.text, 'lxml')
                else:
                    return all_products_urls

        except Exception as e:
            print(f"ERREUR sur gat_all_category: {e}")
            return False

    def product_parser(self):
        """Extraire les infos d'un produit à partir de son URL.

            Args:
                requests.models.response(obj): Contient le code HTML de l'URL dans un objet requests.

        :return:
            dict: Un dictionaire des caractéristiques du produit.
        """
        try:
            soup = BeautifulSoup(self.response.text, 'lxml')
            self.category = soup.find("ul", class_="breadcrumb").findAll("a")[2].text
            article = soup.find("article", class_="product_page")
            self.image_url = "/".join(self.product_page_url.split('/')[:3]) + article.img['src'][5:]
            self.title = article.find("div", class_="col-sm-6 product_main").h1.text
            self.number_available = int("".join([i for i in article.find('p',
                                                                         class_="instock availability").text.strip() if
                                                 i.isdigit()]))
            self.product_description = article.findAll("p")[3].text

            sub_table = article.find("table", class_="table table-striped").findAll("td")
            self.universal_product_code = sub_table[0].text
            self.price_excluding_tax = sub_table[2].text
            self.price_including_tax = sub_table[3].text
            self.review_rating = sub_table[6].text

        except Exception as e:
            print(f"ERREUR sur product_parser: {e}, URL: {self.product_page_url}")
            return False

        product_infos = {"product_page_url": self.product_page_url,
                         "universal_product_code": self.universal_product_code,
                         "title": self.title,
                         "price_including_tax": self.price_including_tax,
                         "price_excluding_tax": self.price_excluding_tax,
                         "number_available": self.number_available,
                         "product_description": self.product_description,
                         "category": self.category,
                         "review_rating": self.review_rating,
                         "image_url": self.image_url
                         }

        return product_infos
