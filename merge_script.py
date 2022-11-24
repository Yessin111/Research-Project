import csv
import json
import urllib.request
import threading

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from unidecode import unidecode

values = []
count = 0


# Add Goodreads ISBNs to list
def create_isbn_list():
    isbn_list = []

    with open("data/goodreads.json", 'r') as file_json:
        for row in file_json:
            isbn = json.loads(row)["isbn"]

            if isbn != "":
                isbn_list.append(isbn)

    return isbn_list


# Use openlibrary API to retrieve the title and author given an ISBN
def openlibrary_info(isbn, lock):
    global count
    with lock:
        count = count + 1
        if count % 100 == 0:
            print(str(count) + " books done")

    try:
        with urllib.request.urlopen("https://openlibrary.org/isbn/" + isbn + ".json") as url_book:
            data_book = json.load(url_book)
            title_ol = unidecode(data_book["title"].split("(")[0].split("[")[0].split("\r\n")[0].strip())

            with urllib.request.urlopen("https://covers.openlibrary.org/b/isbn/" + isbn + "-L.jpg") as input_image:
                arr = np.asarray(bytearray(input_image.read()), dtype=np.uint8)
                if arr.nbytes < 1000:
                    print(str(isbn) + " - Image too small")
                    pass

            if "authors" in data_book:
                with urllib.request.urlopen("https://openlibrary.org" + data_book["authors"][0]["key"] + ".json") as url_author:
                    data_author = json.load(url_author)
                    author_ol = unidecode(data_author["name"].strip())
            else:
                author_ol = "AUTHOR_MISSING_OL"

            az_info = amazon_info(isbn)
            if isinstance(az_info, str):
                print(str(isbn) + " - " + az_info)
                pass
            else:
                with lock:
                    new_value = {
                        "isbn": isbn,
                        "title_ol": title_ol,
                        "title_az": az_info[0],
                        "author_ol": author_ol,
                        "author_az": az_info[1],
                        "reading_age": az_info[2],
                        "grade": az_info[3],
                    }
                    values.append(new_value)
                    print(str(isbn))

    except Exception as e:
        print(str(isbn) + " - " + str(e))
        pass


def amazon_info(isbn):
    s = Service("chromedriver.exe")
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    # options.binary_location("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    browser = webdriver.Chrome(service=s, options=options)
    url_search = "https://www.amazon.com/s?k="+isbn
    browser.get(url_search)
    try:
        url_book = browser.find_element(By.CLASS_NAME, "s-search-results").find_element(By.CSS_SELECTOR, "[data-index=\"1\"]").find_element(By.CSS_SELECTOR, "[href]").get_property("href")
        browser.get(url_book)
        try:
            language = unidecode(browser.find_element(By.ID, "rpi-attribute-language").find_element(By.CLASS_NAME, "rpi-attribute-value").get_attribute("textContent").strip())
        except:
            language = "English"

        if language != "English":
            return "Amazon not English"
        else:
            try:
                title_az = unidecode(browser.find_element(By.ID, "productTitle").get_attribute("textContent").split("(")[0].split("[")[0].replace("®", "").strip())
            except:
                return "Amazon no title"
            try:
                author_az = unidecode(browser.find_element(By.CLASS_NAME, "author").find_element(By.CLASS_NAME, "a-link-normal").get_attribute("textContent").strip())
                if "Visit Amazon's" in author_az:
                    author_az = author_az.split("Visit Amazon's ")[1].split(" Page")[0]
            except:
                author_az = "AUTHOR_MISSING_AZ"
            try:
                reading_age = unidecode(browser.find_element(By.ID, "rpi-attribute-book_details-customer_recommended_age").find_element(By.CLASS_NAME, "rpi-attribute-value").get_attribute("textContent").split(", from customers")[0].strip())
            except:
                reading_age = "READINGAGE_MISSING_AZ"
            try:
                grade = unidecode(browser.find_element(By.ID, "rpi-attribute-book_details-grade_level").find_element(By.CLASS_NAME, "rpi-attribute-value").get_attribute("textContent").strip())
            except:
                grade = "GRADE_MISSING_AZ"

            if reading_age == "READINGAGE_MISSING_AZ" and grade == "GRADE_MISSING_AZ":
                return "Amazon no age"

            return title_az, author_az, reading_age, grade
    except:
        return "Amazon acting up"


def write_to_file():
    with open("data/combined_dataset.csv", 'a', newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=";")
        for value in values:
            try:
                writer.writerow([value["isbn"], value["title_ol"], value["title_az"], value["author_ol"], value["author_az"], value["reading_age"], value["grade"]])
            except:
                pass


# Goodreads
def merge_goodreads(threads, partition_size, partition):
    print()
    print("-------------------------------------------------------")
    print("Processing partition " + str(partition))
    print("-------------------------------------------------------")
    global values
    values = []
    isbn_list = create_isbn_list()[(partition-1)*partition_size:partition*partition_size]

    chunks = [isbn_list[i * threads:(i + 1) * threads] for i in range((len(isbn_list) + threads - 1) // threads)]

    lock = threading.Lock()

    for chunk in chunks:
        threads = []
        for isbn in chunk:
            thread = threading.Thread(target=openlibrary_info, args=(isbn, lock,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    write_to_file()
