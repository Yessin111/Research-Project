# import urllib
#
# from google.cloud import vision
# from google.oauth2 import service_account
#
# try:
#     credentials = service_account.Credentials.from_service_account_file("../google-key.json")
#     client = vision.ImageAnnotatorClient(credentials=credentials)
#
#     with urllib.request.urlopen("https://m.media-amazon.com/images/I/71gkoniITpL.jpg") as input_image:
#         content = input_image.read()
#         image = vision.Image(content=content)
#
#     response = client.object_localization(image=image)
#     print(response)
#
# except Exception as e:
#     print(e)
