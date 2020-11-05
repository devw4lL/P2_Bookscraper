
from pprint import pprint
from packages.html_parser import HtmlParser
from packages.csv import Csv
from packages.images import Images
from pprint import pprint
url = "http://books.toscrape.com/"
all_products_urls = {}
data_write = []


if __name__ == "__main__":
    buff = [] #Buufer pour les infos produits de chaque catégorie
    P = HtmlParser(url)
    CSV = Csv(buff)
    I = Images(CSV.date)
    if P.get_response(): #Vérifie code 200 sur URL de base
        all_categorys = P.get_all_category() #Récupère les URLs de chaque catégorie
        for category in all_categorys:
            P.product_page_url = category
            if P.get_response(): #Vérifie l'url de la catégorie en cours
                for all_urls in P.extract_products_urls(): #Récupère toutes les urls produit par catégories et itère dessus
                    P.product_page_url = all_urls
                    if P.get_response():
                        buff.append(P.product_parser()) #Ajoute au buffer de la catégorie en cours les infos produits
                        #pprint(buff, indent=4)
                        I.ImageDownload(P.image_url, P.category, P.title)
                CSV.data = buff
                CSV.csv_write() #Ecrit le fichier CSV de la catégorie
                buff = [] #Vide le buffer pour la prochaine catégorie


def old():
    def csv_write(data):
        csv_columns = ["product_page_url",
                       "universal_product_code",
                       "title",
                       "price_including_tax",
                       "price_excluding_tax",
                       "number_available",
                       "product_description",
                       "category",
                       "review_rating",
                       "image_url"]

        file_name = data['category'] + "_" + str(datetime.today()).split()[0]
        print(file_name)
        path = os.path.join(os.path.dirname(__file__), "results", file_name + ".csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(data)


    def get_products_urls(url):
        res = HtmlParser(url)
        if res.get_response():
            all_categorys_urls = res.get_all_category()
            for category in all_categorys_urls[:2]:
                res.product_page_url = category
                if res.get_response():
                    for all_urls in res.extract_products_urls():
                        all_products_urls.append(all_urls)



        return all_products_urls

    get_products_urls(url)

    for product_url in all_products_urls:
        ress = HtmlParser(product_url)
        if ress.get_response():
            data_write.append(ress.product_parser())

    for data in data_write:
        csv_write(data)




"""
http://books.toscrape.com/

"product_page_url",
"universal_ product_code (,upc)"
"title",
"price_including_tax",
"price_excluding_tax",
"number_available",
"product_description",
"category",
"review_rating",
"image_url",

Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.

"""
