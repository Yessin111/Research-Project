import os.path
import urllib.request
import gzip
import shutil
import csv

goodreads_child_url = "https://drive.google.com/uc?id=1R3wJPgyzEX9w6EI8_LmqLbpY4cIC9gw4&confirm=t&uuid=e347bf6e-fbf4-48b0-a732-70c0309e58a2&at=ALAFpqzaZEeR0vKTgxLid4jqSb6A:1667130831307"
goodreads_ya_url = "https://drive.google.com/uc?id=1gH7dG4yQzZykTpbHYsrw2nFknjUm0Mol&confirm=t&uuid=d48264f8-8951-461e-ba25-678db6402a3d&at=AHV7M3ccxlZ2i4-jYFR3HV7X9odQ:1669322057685"


def initialize(root):
    if not os.path.exists(root + "/data"):
        os.makedirs(root + "/data")
    if not os.path.isfile(root + "/data/combined_dataset_child.csv"):
        with open(root + "/data/combined_dataset_child.csv", 'w', newline='') as f:
            wr = csv.writer(f, delimiter=";")
            wr.writerow(["isbn", "title_ol", "title_az", "author_ol", "author_az", "reading_age", "grade"])
    if not os.path.isfile(root + "/data/combined_dataset_ya.csv"):
        with open(root + "/data/combined_dataset_ya.csv", 'w', newline='') as f:
            wr = csv.writer(f, delimiter=";")
            wr.writerow(["isbn", "title_ol", "title_az", "author_ol", "author_az", "reading_age", "grade"])


def download_gz(source_url, target_name, data_extension, root):
    if not os.path.isfile(root + "/data/"+target_name+"."+data_extension):
        # Download file
        print("downloading "+target_name+"...")
        urllib.request.urlretrieve(source_url, root + "/data/" + target_name + "_source."+data_extension+".gz")

        # Extract file
        print("extracting " + target_name + "...")
        with gzip.open(root + "/data/" + target_name + "_source."+data_extension+".gz", 'rb') as f_in:
            with open(root + "/data/" + target_name + "."+data_extension, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Finish
        os.remove(root + "/data/" + target_name + "_source."+data_extension+".gz")
        print(target_name+" complete\n")


def download_all(root):
    initialize(root)
    download_gz(goodreads_child_url, "goodreads_child", "json", root)
    download_gz(goodreads_ya_url, "goodreads_ya", "json", root)
