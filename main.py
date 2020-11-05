from packages.html_parser import HtmlParser
from packages.csv import Csv
from packages.images import Images


url = "http://books.toscrape.com/"

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
                        I.ImageDownload(P.image_url, P.category, P.title)
                CSV.data = buff
                CSV.csv_write() #Ecrit le fichier CSV de la catégorie
                buff = [] #Vide le buffer pour la prochaine catégorie

