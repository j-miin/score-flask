import cloudinary
import cloudinary.uploader
import os


def uploader(image_string):
    cloudinary.config(
        cloud_name=os.environ['CLOUDINARY_NAME'],
        api_key=os.environ['CLOUDINARY_KEY'],
        api_secret=os.environ['CLOUDINARY_SECRET']
    )
    result = cloudinary.uploader.upload(image_string)
    return result['public_id']
