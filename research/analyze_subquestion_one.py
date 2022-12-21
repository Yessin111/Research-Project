import json


def mapper(data, count):
    return round(round(data, 3)/count, 3)


def analyze(root):

    amazon_count = [0, 0, 0, 0, 0]
    amazon_brightness = [0, 0, 0, 0, 0]
    amazon_colorfulness = [0, 0, 0, 0, 0]
    amazon_contrast = [0, 0, 0, 0, 0]
    amazon_entropy = [0, 0, 0, 0, 0]

    with open(root + "/data/data_subquestion_one.json", 'r') as file_json:
        json_data = json.load(file_json)

        for row in json_data:
            if "sq1" in row["amazon"]:
                for i in range(5):
                    if i in row["age"]:
                        amazon_count[i] = amazon_count[i] + 1
                        amazon_brightness[i] = amazon_brightness[i] + row["amazon"]["sq1"]["brightness"]
                        amazon_colorfulness[i] = amazon_colorfulness[i] + row["amazon"]["sq1"]["colorfulness"]
                        amazon_contrast[i] = amazon_contrast[i] + row["amazon"]["sq1"]["contrast"]
                        amazon_entropy[i] = amazon_entropy[i] + row["amazon"]["sq1"]["entropy"]

    print(list(map(mapper, amazon_brightness, amazon_count)))
    print(list(map(mapper, amazon_colorfulness, amazon_count)))
    print(list(map(mapper, amazon_contrast, amazon_count)))
    print(list(map(mapper, amazon_entropy, amazon_count)))

