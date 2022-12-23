import json
import matplotlib.pyplot as plt
import numpy as np


def mapper(data, count):
    return round(round(data, 3)/count, 3)


def plot(data):
    # plt.boxplot(data)
    #
    # plt.xlabel('x values')
    # plt.ylabel('y values')
    # plt.title('plotted x and y values')
    # plt.legend(['line 1'])
    # # plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    # plt.show()

    fig, ax = plt.subplots()
    ax.boxplot(my_dict.values())
    ax.set_xticklabels(my_dict.keys())


def analyze(root):
    amazon_count = [0, 0, 0, 0, 0]
    amazon_brightness = [[], [], [], [], []]
    amazon_colorfulness = [[], [], [], [], []]
    amazon_contrast = [[], [], [], [], []]
    amazon_entropy = [[], [], [], [], []]

    with open(root + "/data/data_subquestion_one.json", 'r') as file_json:
        json_data = json.load(file_json)

        for row in json_data:
            if "sq1" in row["amazon"]:
                for i in range(5):
                    if i in row["age"]:
                        amazon_count[i] = amazon_count[i] + 1
                        amazon_brightness[i].append(row["amazon"]["sq1"]["brightness"])
                        amazon_colorfulness[i].append(row["amazon"]["sq1"]["colorfulness"])
                        amazon_contrast[i].append(row["amazon"]["sq1"]["contrast"])
                        amazon_entropy[i].append(row["amazon"]["sq1"]["entropy"])

    plot(amazon_brightness[0])
