import requests
import shutil

# url = "https://books.am/media/catalog/product/placeholder/default/Books_Default_image.jpg"

# r = requests.get(url=url, stream=True)
# if r.status_code == 200:
#     with open("static/images/img.jpg", 'wb') as f:
#         r.raw.decode_content = True
#         a = shutil.copyfileobj(r.raw, f)
#         print(a)


def dow_img(url, filename):
    req = requests.get(url=url, stream=True)
    if req.status_code == 200:
        with open(f"static/images/{filename}.jpg", "wb") as f:
            req.raw.decode_content = True
            cop = shutil.copyfileobj(req.raw, f)
    return filename


# dow_img(url=url, filename="standart")

