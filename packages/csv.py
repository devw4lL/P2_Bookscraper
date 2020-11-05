import csv
import os

from datetime import datetime


class Csv:
    def __init__(self, data):
        self.data = data
        self.date = str(str(datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0])

    def csv_write(self):
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

        file_name = self.data[0]['category']
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "result", self.date)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                print(f"ERREUR dans csv_write: {e}")
                return False
        else:
            full_path = os.path.join(path, file_name + ".csv")
            with open(full_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns)
                writer.writeheader()
                [writer.writerow(product) for product in self.data]




