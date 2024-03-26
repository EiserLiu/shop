import base64
import io
from os import path

import numpy as np
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from rest_framework import status
from rest_framework.response import Response





if __name__ == '__main__':
    Image1 = open("../file/image/posters1.jpg")
    Image2 = open("../file/image/posters2.jpg")

    print(type(Image1))
    print(type(Image2))

    imageS = ImageSimilarity()
    imageS.compare_images(Image1, Image2)
