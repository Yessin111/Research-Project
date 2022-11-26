import json


def analyze(root):

    amount = [0, 0, 0, 0, 0]
    brightness_list = [0, 0, 0, 0, 0]
    colorfulness_list = [0, 0, 0, 0, 0]
    init = False
    brightness_lowest = -1
    brightness_highest = -1
    colorfulness_lowest = -1
    colorfulness_highest = -1

    with open(root + "/data/data_subquestion_one.json", 'r') as file_json:
        json_data = json.load(file_json)
        for row in json_data:
            age = row["age"]
            brightness = row["brightness"]
            colorfulness = row["colorfulness"]

            if not init:
                brightness_lowest = brightness
                brightness_highest = brightness
                colorfulness_lowest = colorfulness
                colorfulness_highest = colorfulness
                init = True
            else:
                if brightness < brightness_lowest:
                    brightness_lowest = brightness
                if brightness > brightness_highest:
                    brightness_highest = brightness
                if colorfulness < colorfulness_lowest:
                    colorfulness_lowest = colorfulness
                if colorfulness > colorfulness_highest:
                    colorfulness_highest = colorfulness

            for i in range(5):
                if i in age:
                    amount[i] = amount[i] + 1
                    brightness_list[i] = brightness_list[i] + brightness
                    colorfulness_list[i] = colorfulness_list[i] + colorfulness

    for i in range(5):
        brightness_list[i] = round(brightness_list[i] / amount[i], 3)

    print(colorfulness)
    print(colorfulness_lowest)
    print(colorfulness_highest)
