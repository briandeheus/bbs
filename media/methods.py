import os
import secrets
from io import BytesIO

import boto3
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    endpoint_url=settings.AWS_S3_ENDPOINT,
)


def generate_unique_name(file_name):
    # Generate a cryptographically secure random string of 12 characters
    random_string = secrets.token_hex(6)  # 6 bytes = 12 hexadecimal characters
    # Extract the file extension and append it to the random string
    file_extension = os.path.splitext(file_name)[1]
    new_file_name = f"{random_string}{file_extension}"
    return new_file_name


def create_thumbnail(uploaded_file, max_dimension=600):
    # Open the image using PIL
    image = Image.open(uploaded_file)

    # Create a thumbnail maintaining the aspect ratio
    image.thumbnail((max_dimension, max_dimension))

    # Convert image to bytes
    buffer = BytesIO()
    image_name = generate_unique_name(file_name="foo.png")
    image.save(buffer, format="png")

    # Convert bytes back to Django's InMemoryUploadedFile
    thumbnail_file = InMemoryUploadedFile(
        buffer,
        "ImageField",
        f"thumbnail_{image_name}",
        uploaded_file.content_type,
        buffer.tell,
        None,
    )

    thumbnail_file.seek(0)
    return thumbnail_file


def upload_to_s3(uploaded_file):
    # Extract the file extension and append it to the random string
    s3_file_name = generate_unique_name(file_name=uploaded_file.name)

    s3_client.upload_fileobj(
        uploaded_file,
        settings.AWS_BUCKET_NAME,
        s3_file_name,
        ExtraArgs={"ContentType": uploaded_file.content_type},
    )

    url = f"https://{settings.AWS_CDN_URL}/{s3_file_name}"
    return url
