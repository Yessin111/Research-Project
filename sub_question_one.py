import urllib.request
import cv2
import numpy as np
import skimage.measure
from PIL import Image, ImageStat
from sklearn.cluster import KMeans
from color_names import color_names


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
    return round(contrast / 100, 3)


# https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
def get_entropy(input_image):
    entropy = skimage.measure.shannon_entropy(input_image)
    return round(entropy / 100, 3)


def get_all():
    isbn = "1841489611"
    with urllib.request.urlopen("https://covers.openlibrary.org/b/isbn/" + isbn + "-L.jpg") as input_image:
        arr = np.asarray(bytearray(input_image.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)

        dominant_color = get_dominant_color(image)
        brightness = get_brightness(image)
        colorfulness = get_colorfulness(image)
        contrast = get_contrast(image)
        entropy = get_entropy(image)

        print(dominant_color)
        print(brightness)
        print(colorfulness)
        print(contrast)
        print(entropy)

        cv2.imshow(isbn, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


get_all()
