import os
import requests
import re

from shutil import copyfileobj


class Images:
    """Traitement des images

        Args:
            URL (str): URL de l'image à traiter.

        Returns:
            Sauvergarde l'image dans le dosssier ~/results/date_heure/category/
    """
    def __init__(self, date):
        self.date = date
        self.url = ""
        self.category = ""
        self.title = ""

    def ImageDownload(self, url, category, title):
        """Télecharger et enregistrer des images.

        :param url: URL de l'image.
        :param category: categorie de livre en cours d'analyse.
        :param title: titre du livre == titre de l'image sauvgardé.
        :return:
            Sauvergarde l'image dans le dosssier ~/results/date_heure/category/
        """
        self.url, self.category, self.title = url, category, title
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "result", self.date, self.category)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                print(f"ERREUR dans csv_write: {e}")
                return False

        img = requests.get(self.url, stream=True)
        if img.ok:
            p = re.compile(r'[^a-zA-Z0-9 -]')
            self.title = p.sub('_', self.title)
            full_path = os.path.join(path, self.title + ".jpg")
            with open(full_path, 'wb') as f:
                img.raw.decode_content = True
                copyfileobj(img.raw, f)
