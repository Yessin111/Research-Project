import threading
import urllib.request
import cv2
import json
import skimage.measure
import numpy as np
from PIL import Image, ImageStat
from sklearn.cluster import KMeans
from research.color_names import color_names

dictionary = []


# https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def get_color_name(rgb_triplet):
    min_colours = {}
    for row in color_names:
        r_c, g_c, b_c = list(row.keys())[0]
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = list(row.values())[0]
    return min_colours[min(min_colours.keys())]


# https://medium.com/buzzrobot/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036
def get_dominant_color(input_image):
    img = input_image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    kmeans = KMeans(9)
    kmeans.fit(img)
    color = abs(kmeans.cluster_centers_.round())[np.bincount(kmeans.labels_).argmax()]
    color = (int(color[0]), int(color[1]), int(color[2]))
    color_name = get_color_name(color)
    return color, color_name


# https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
def get_brightness(input_image):
    brightness_image = Image.fromarray(input_image).convert("L")
    stat = ImageStat.Stat(brightness_image)
    return round(stat.mean[0] / 255, 3)


# https://pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/
# https://stackoverflow.com/questions/55662369/mathematical-calculation-for-colorfulness-of-image-color-theory
def get_colorfulness(input_image):
    (R, G, B) = cv2.split(input_image.astype("float"))
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    std_root = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    mean_root = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # return round((std_root + (0.3 * mean_root)) / 100, 3)
    return round((std_root + (0.3 * mean_root)), 3)


# https://stackoverflow.com/questions/58821130/how-to-calculate-the-contrast-of-an-image
def get_contrast(input_image):
    contrast_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    contrast = contrast_image.std()
    return round(contrast, 3)


# https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
def get_entropy(input_image):
    entropy = skimage.measure.shannon_entropy(input_image)
    return round(entropy, 3)


def get_all(row, lock):
    print(row["isbn"])
    try:
        with urllib.request.urlopen("https://covers.openlibrary.org/b/isbn/" + row["isbn"] + "-L.jpg") as input_image:
            arr = np.asarray(bytearray(input_image.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)

            dom_color = get_dominant_color(image)

            row["dominant_color_rgb"] = dom_color[0]
            row["dominant_color_name"] = dom_color[1]
            row["brightness"] = get_brightness(image)
            row["colorfulness"] = get_colorfulness(image)
            row["contrast"] = get_contrast(image)
            row["entropy"] = get_entropy(image)

            with lock:
                dictionary.append(row)

    except:
        pass


def write_to_file(partition, root):
    if partition == 1 or partition == 600 or partition == 1200:
        open(root + "/data/data_subquestion_one.json", "w")

        with open(root + "/data/data_subquestion_one.json", "r+") as file_json:
            file_json.seek(0)
            json.dump(dictionary, file_json, indent=4)
    else:
        with open(root + "/data/data_subquestion_one.json", "r+") as file_json:
            file_data = json.loads(file_json.read())
            file_data = file_data + dictionary
            file_json.seek(0)
            json.dump(file_data, file_json, indent=4)


def sub_question_one(threads, partition_size, partition, root):
    print()
    print("-------------------------------------------------------")
    print("Processing partition " + str(partition))
    print("-------------------------------------------------------")
    global dictionary
    dictionary = []

    with open(root + "/data/data.json", "r") as file_json:
        json_data = json.load(file_json)

    json_data = json_data[(partition - 1) * partition_size:partition * partition_size]
    chunks = [json_data[i * threads:(i + 1) * threads] for i in range((len(json_data) + threads - 1) // threads)]

    lock = threading.Lock()

    for chunk in chunks:
        threads = []
        for row in chunk:
            thread = threading.Thread(target=get_all, args=(row, lock,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    write_to_file(partition, root)
