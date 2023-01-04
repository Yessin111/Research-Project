import json
import matplotlib.pyplot as plt
import numpy as np
from research.color_names import color_names, color_names_dict


def mapper(data, count):
    return round(round(data, 3)/count, 3)


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


def make_box(data1, data2, name):
    ticks = ['0-3', '4-6', '7-9', '10-12', '13+']

    plt.figure()

    bpl = plt.boxplot(data1, positions=np.array(range(len(data1))) * 2.0 - 0.4, sym='', widths=0.6)
    bpr = plt.boxplot(data2, positions=np.array(range(len(data2))) * 2.0 + 0.4, sym='', widths=0.6)
    set_box_color(bpl, '#FF9900')
    set_box_color(bpr, '#146EB4')

    plt.plot([], c='#FF9900', label='Amazon')
    plt.plot([], c='#146EB4', label='Open Library')
    plt.legend()

    plt.xticks(range(0, len(ticks) * 2, 2), ticks)
    plt.tight_layout()
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    plt.savefig(name)


def make_pie(data, name):
    labels = []
    sizes = []
    colors = []
    key_list = list(color_names_dict.keys())
    val_list = list(color_names_dict.values())

    for (x, y) in data:
        labels.append(x)
        sizes.append(y)
        colors.append('#%02x%02x%02x' % key_list[val_list.index(x)])

    bars = plt.bar(labels, sizes)

    i = 0
    for c in colors:
        bars[i].set_color(colors[i])
        i = i + 1

    plt.show()


def analyze(root):
    amazon_count = [0, 0, 0, 0, 0]
    amazon_colors = [{}, {}, {}, {}, {}]
    amazon_brightness = [[], [], [], [], []]
    amazon_colorfulness = [[], [], [], [], []]
    amazon_contrast = [[], [], [], [], []]
    amazon_entropy = [[], [], [], [], []]
    library_count = [0, 0, 0, 0, 0]
    library_colors = [{}, {}, {}, {}, {}]
    library_brightness = [[], [], [], [], []]
    library_colorfulness = [[], [], [], [], []]
    library_contrast = [[], [], [], [], []]
    library_entropy = [[], [], [], [], []]

    with open(root + "/data/data_subquestion_one.json", 'r') as file_json:
        json_data = json.load(file_json)

        for row in json_data:
            if "sq1" in row["amazon"]:
                for i in range(5):
                    if i in row["age"]:
                        amazon_count[i] = amazon_count[i] + 1
                        amazon_colors[i][row["amazon"]["sq1"]["dominant_color_name"]] = amazon_colors[i].get(row["amazon"]["sq1"]["dominant_color_name"], 0) + 1
                        amazon_brightness[i].append(row["amazon"]["sq1"]["brightness"])
                        amazon_colorfulness[i].append(row["amazon"]["sq1"]["colorfulness"])
                        amazon_contrast[i].append(row["amazon"]["sq1"]["contrast"])
                        amazon_entropy[i].append(row["amazon"]["sq1"]["entropy"])
            if "sq1" in row["library"]:
                for i in range(5):
                    if i in row["age"]:
                        library_count[i] = library_count[i] + 1
                        library_colors[i][row["library"]["sq1"]["dominant_color_name"]] = library_colors[i].get(row["library"]["sq1"]["dominant_color_name"], 0) + 1
                        library_brightness[i].append(row["library"]["sq1"]["brightness"])
                        library_colorfulness[i].append(row["library"]["sq1"]["colorfulness"])
                        library_contrast[i].append(row["library"]["sq1"]["contrast"])
                        library_entropy[i].append(row["library"]["sq1"]["entropy"])

    # make_box(amazon_brightness, library_brightness, "brightness")
    # make_box(amazon_colorfulness, library_colorfulness, "colorfulness")
    # make_box(amazon_contrast, library_contrast, "contrast")
    # make_box(amazon_entropy, library_entropy, "entropy")

    for i in range(5):
        amazon_colors[i] = sorted(amazon_colors[i].items(), key=lambda x: x[1], reverse=True)
        library_colors[i] = sorted(library_colors[i].items(), key=lambda x: x[1], reverse=True)

    make_pie(amazon_colors[0], "amazon_color_0")
