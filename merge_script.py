import csv
import json
import urllib.request
import requests
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
    try:
        with urllib.request.urlopen("https://openlibrary.org/isbn/" + isbn + ".json") as url_book:
            data_book = json.load(url_book)
            title_ol = data_book["title"].strip()

            if "authors" in data_book:
                with urllib.request.urlopen("https://openlibrary.org" + data_book["authors"][0]["key"] + ".json") as url_author:
                    data_author = json.load(url_author)
                    author_ol = data_author["name"].strip()
            else:
                author_ol = "AUTHOR_MISSING_OL"

            az_info = amazon_info(isbn)

            with lock:
                count = count + 1
                if count % 1000 == 0:
                    print(str(count) + " books done...")

                if not az_info:
                    pass
                else:
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


    except:
        with lock:
            count = count + 1
            if count % 1000 == 0:
                print(str(count) + " books done...")


def amazon_info(isbn):
    s = Service("chromedriver.exe")
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=s, options=options)
    url_search = "https://www.amazon.com/s?k="+isbn
    browser.get(url_search)
    url_book = browser.find_element(By.CLASS_NAME, "s-search-results").find_element(By.CSS_SELECTOR,"[data-index=\"1\"]").find_element(By.CSS_SELECTOR, "[href]").get_property("href")
    browser.get(url_book)
    try:
        language = browser.find_element(By.ID, "rpi-attribute-language").find_element(By.CLASS_NAME,"rpi-attribute-value").get_attribute("textContent").strip()
    except:
        language = "English"

    if language != "English":
        return False
    else:
        try:
            title_az = browser.find_element(By.ID, "productTitle").get_attribute("textContent").strip()
        except:
            return False
        try:
            author_az = browser.find_element(By.CLASS_NAME, "author").find_element(By.CLASS_NAME,"a-link-normal").get_attribute("textContent").strip()
            if "Visit Amazon's" in author_az:
                author_az = author_az.split("Visit Amazon's ")[1].split(" Page")[0]
        except:
            author_az = "AUTHOR_MISSING_AZ"
        try:
            reading_age = browser.find_element(By.ID, "rpi-attribute-book_details-customer_recommended_age").find_element(By.CLASS_NAME, "rpi-attribute-value").get_attribute("textContent").split(", from customers")[0].strip()
        except:
            reading_age = "READINGAGE_MISSING_AZ"
        try:
            grade = browser.find_element(By.ID, "rpi-attribute-book_details-grade_level").find_element(By.CLASS_NAME,"rpi-attribute-value").get_attribute("textContent").strip()
        except:
            grade = "GRADE_MISSING_AZ"

        if reading_age == "READINGAGE_MISSING_AZ" and grade == "GRADE_MISSING_AZ":
            return False

        return title_az, author_az, reading_age, grade


def write_to_file():
    with open("data/combined_dataset.csv", 'a', newline='') as file_csv:
        writer = csv.writer(file_csv, delimiter=";")
        for value in values:
            try:
                writer.writerow([value["isbn"], value["title_ol"], value["title_az"], value["author_ol"], value["author_az"], value["reading_age"], value["grade"]])
            except:
                pass


# Goodreads
def merge_goodreads():
    isbn_list = create_isbn_list()
    print("Processing " + str(len(isbn_list)) + " books...")
    isbn_list = isbn_list[0:50]

    n = 10
    chunks = [isbn_list[i * n:(i + 1) * n] for i in range((len(isbn_list) + n - 1) // n)]

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
