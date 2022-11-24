import os.path
import urllib.request
import gzip
import shutil
import csv

goodreads_url = "https://drive.google.com/uc?id=1R3wJPgyzEX9w6EI8_LmqLbpY4cIC9gw4&confirm=t&uuid=e347bf6e-fbf4-48b0-a732-70c0309e58a2&at=ALAFpqzaZEeR0vKTgxLid4jqSb6A:1667130831307"


def initialize():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.isfile("data/combined_dataset.csv"):
        with open("data/combined_dataset.csv", 'w', newline='') as f:
            wr = csv.writer(f, delimiter=";")
            wr.writerow(["isbn", "title_ol", "title_az", "author_ol", "author_az", "reading_age", "grade"])


def download_gz(source_url, target_name, data_extension):
    if not os.path.isfile("data/"+target_name+"."+data_extension):
        # Download file
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, "data/" + target_name + "_source."+data_extension+".gz")

        # Extract file
        print("extracting " + target_name + "...")
        with gzip.open("data/" + target_name + "_source."+data_extension+".gz", 'rb') as f_in:
            with open("data/" + target_name + "."+data_extension, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Finish
        os.remove("data/" + target_name + "_source."+data_extension+".gz")
        print(target_name+" complete\n")


def download_all():
    initialize()
    download_gz(goodreads_url, "goodreads", "json")
