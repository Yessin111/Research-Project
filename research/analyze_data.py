import csv
import re
from difflib import SequenceMatcher


def check_new_classification():
    with open("../data/combined_dataset.csv", newline='') as file_csv:
        reader = csv.reader(file_csv, delimiter=';')
        next(reader)

        age_dict = [0, 0, 0, 0, 0]

        for row in reader:
            age = row[5]

            if age != "READINGAGE_MISSING_AZ":
                age = age.replace("Baby", str(1))

                if age.__contains__("+") or age.__contains__("and up"):
                    age = age.split("+")[0]
                    num1 = [int(i) for i in age.split() if i.isdigit()][0]
                    num2 = num1 + 2

                else:
                    age = age.split(" years")[0]
                    nums = [int(i) for i in age.split() if i.isdigit()]
                    if nums[0] >= nums[1]-4:
                        num1 = nums[0]
                        num2 = nums[1]
                    else:
                        num1 = 99
                        num2 = 99

                if int(num1) <= 3:
                    age_dict[0] = age_dict[0] + 1
                elif 4 <= int(num1) <= 6:
                    age_dict[1] = age_dict[1] + 1
                elif 7 <= int(num1) <= 9:
                    age_dict[2] = age_dict[2] + 1
                elif 10 <= int(num1) <= 12:
                    age_dict[3] = age_dict[3] + 1
                elif 13 <= int(num1) <= 18:
                    age_dict[4] = age_dict[4] + 1
                else:
                    pass

                if int(num2) <= 3:
                    age_dict[0] = age_dict[0] + 1
                elif 4 <= int(num2) <= 6:
                    age_dict[1] = age_dict[1] + 1
                elif 7 <= int(num2) <= 9:
                    age_dict[2] = age_dict[2] + 1
                elif 10 <= int(num2) <= 12:
                    age_dict[3] = age_dict[3] + 1
                elif 13 <= int(num2) <= 18:
                    age_dict[4] = age_dict[4] + 1
                else:
                    pass

        # total = sum(age_dict)
        # age_dict[0] = round(age_dict[0] / total, 2)
        # age_dict[1] = round(age_dict[1] / total, 2)
        # age_dict[2] = round(age_dict[2] / total, 2)
        # age_dict[3] = round(age_dict[3] / total, 2)
        # age_dict[4] = round(age_dict[4] / total, 2)
        print(age_dict)


def analyze_age():
    with open("../data/combined_dataset.csv", newline='') as file_csv:
        reader = csv.reader(file_csv, delimiter=';')
        next(reader)
        count = 0

        age_dict = [0, 0, 0, 0, 0]

        for row in reader:
            count = count + 1
            age = row[5]

            if age != "READINGAGE_MISSING_AZ":
                age = age.replace("Baby", str(1))
                age = age.split("+")[0]
                age = age.split(" ")[0]
            else:
                age = row[6]

                replacements = {"Preschool": "5", "Kindergarten": "6", "10": "16", "11": "17", "12": "18",
                                "1": "7", "2": "8", "3": "9", "4": "10", "5": "11", "6": "12", "7": "13",
                                "8": "14", "9": "15"}

                pattern = re.compile("|".join(replacements.keys()))
                age = pattern.sub(lambda m: replacements[re.escape(m.group(0))], age)

                age = age.split(" ")[0]

            if int(age) <= 3:
                age = 0
            elif 4 <= int(age) <= 6:
                age = 1
            elif 7 <= int(age) <= 9:
                age = 2
            elif 10 <= int(age) <= 12:
                age = 3
            elif 13 <= int(age) <= 18:
                age = 4
            else:
                print("Book not valid")

            age_dict[age] = age_dict[age] + 1

        # total = sum(age_dict)
        # age_dict[0] = round(age_dict[0] / total, 2)
        # age_dict[1] = round(age_dict[1] / total, 2)
        # age_dict[2] = round(age_dict[2] / total, 2)
        # age_dict[3] = round(age_dict[3] / total, 2)
        # age_dict[4] = round(age_dict[4] / total, 2)
        print(age_dict)


def analyze_title():
    with open("../data/combined_dataset.csv", newline='') as file_csv:
        reader = csv.reader(file_csv, delimiter=';')
        next(reader)

        rates = []

        for row in reader:
            title_ol = row[1]
            title_az = row[2]

            similarity = SequenceMatcher(None, title_ol, title_az).ratio()
            rates.append((title_ol, title_az, similarity))

        rates = sorted(rates, key=lambda x: x[2])
        print(rates)


analyze_age()
check_new_classification()
