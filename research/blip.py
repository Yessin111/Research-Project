import urllib
import replicate
import os
import sys

sys.path.insert(1, 'C:/Users/Yessin/LAVIS')

with urllib.request.urlopen("https://m.media-amazon.com/images/I/71gkoniITpL.jpg") as input_image:
    content = input_image.read()

model = replicate.models.get("salesforce/blip")
version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")
output = version.predict(image=content)
