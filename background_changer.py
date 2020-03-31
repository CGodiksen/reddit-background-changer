import ctypes
import PIL
from PIL import Image
from win32api import GetSystemMetrics


def resize_image(image, width=GetSystemMetrics(0), height=GetSystemMetrics(1)):
    return image.resize((width, height))


def change_background(directory_path, image_name):
    image = Image.open(directory_path + image_name)
    print(f"Image format: {image.format}\nImage size: {image.size}")

    new_image = resize_image(image)
    new_image.save(directory_path + "background.jpg")

    ctypes.windll.user32.SystemParametersInfoW(20, 0, directory_path + "background.jpg", 0)


directory_path = "C:/Users/chris/PycharmProjects/reddit-desktop-background/images/"
image_name = "cat.jpg"


change_background(directory_path, image_name)
