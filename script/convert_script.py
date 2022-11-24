import csv
import json
import os
import re


def analyze_age(reading_age, grade):
    result = []
    if reading_age != "READINGAGE_MISSING_AZ":
        age = reading_age.replace("Baby", str(1))

        if age.__contains__("+") or age.__contains__("and up"):
            age = age.split("+")[0]
            num1 = [int(i) for i in age.split() if i.isdigit()][0]
            num2 = num1 + 2
        else:
            age = age.split(" years")[0]
            nums = [int(i) for i in age.split() if i.isdigit()]
            num1 = nums[0]
            num2 = nums[1]
    else:
        replacements = {"Baby": "1", "Preschool": "5", "Kindergarten": "6", "10": "16", "11": "17", "12": "18",
                        "1": "7", "2": "8", "3": "9", "4": "10", "5": "11", "6": "12", "7": "13",
                        "8": "14", "9": "15"}

        pattern = re.compile("|".join(replacements.keys()))
        age = pattern.sub(lambda m: replacements[re.escape(m.group(0))], grade)

        if age.__contains__("+") or age.__contains__("and up"):
            age = age.split("+")[0]
            num1 = [int(i) for i in age.split() if i.isdigit()][0]
            num2 = num1 + 2
        else:
            nums = [int(i) for i in age.split() if i.isdigit()]
            num1 = nums[0]
            num2 = nums[1]

    if num1 <= 3 or num2 <= 3:
        result.append(0)
    if 4 <= num1 <= 6 or 4 <= num2 <= 6 or num1 <= 4 and 6 <= num2:
        result.append(1)
    if 7 <= num1 <= 9 or 7 <= num2 <= 9 or num1 <= 7 and 9 <= num2:
        result.append(2)
    if 10 <= num1 <= 12 or 10 <= num2 <= 12 or num1 <= 10 and 12 <= num2:
        result.append(3)
    if num1 >= 13 or num2 >= 13:
        result.append(4)

    if num1 < num2 - 4:
        print(str(num1) + " " + str(num2))
        print(len(result))
        print(result)
        print()

    if len(result) >= 3:
        return False

    return result


def convert_data(root):
    total = 0
    good = 0
    if not os.path.isfile(root + "/data/data.json"):
        dictionary = []

        with open(root + "/data/combined_dataset_child.csv", newline='') as file_csv:
            reader = csv.reader(file_csv, delimiter=';')
            next(reader)

            for row in reader:
                total = total + 1
                age = analyze_age(row[5], row[6])
                if not age:
                    pass
                else:
                    good = good + 1
                    entry = {
                        "isbn": row[0],
                        "age": age,
                    }

                    dictionary.append(entry)

        with open(root + "/data/data.json", "w") as file_json:
            json_object = json.dumps(dictionary, indent=4)
            file_json.write(json_object)

    print(total)
    print(good)
