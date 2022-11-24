import csv
import json


def convert_data():
    dictionary = []

    with open("data/combined_dataset.csv", newline='') as file_csv:
        reader = csv.reader(file_csv, delimiter=';')
        next(reader)

        for row in reader:
            entry = {
                "isbn": row[0],
                "title_openlibrary": row[1],
                "title_amazon": row[2],
                "author_openlibrary": row[3],
                "author_amazon": row[4],
                "reading_age": row[5],
                "grade": row[6]
            }

            dictionary.append(entry)

    with open("data/data.json", "w") as file_json:
        json_object = json.dumps(dictionary, indent=4)
        file_json.write(json_object)


convert_data()
