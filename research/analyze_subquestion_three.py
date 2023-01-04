import json


def analyze(root):
    isbn = []

    with open(root + "/data/data_subquestion_three.json", 'r') as file_json:
        json_data = json.load(file_json)
        y = len(json_data)

        for row in json_data:
            if row["isbn"] not in isbn:
                isbn.append(row["isbn"])
            else:
                print("SCREAM")
            if "sq3" in row["amazon"]:
                for i in range(5):
                    if i in row["age"]:
                        pass
            if "sq3" in row["library"]:
                for i in range(5):
                    if i in row["age"]:
                        pass

    print(y)