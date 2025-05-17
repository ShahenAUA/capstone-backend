import uuid
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from pet_welfare.settings import MAX_FILE_WIDTH, MAX_FILE_HEIGHT

def process_uploaded_image(instance, image_field_name, image, prefix, max_picture_width=MAX_FILE_WIDTH, max_picture_height=MAX_FILE_HEIGHT):
    # if image.size > MAX_FILE_SIZE_MB * 1024 * 1024:
    #     raise ValidationError({image_field_name: FILE_SIZE_EXCEEDS_MAX_SIZE})
    
    img = Image.open(image)
    
    if img.format != 'JPEG':
        image = convert_image_to_jpg(img)
        img = Image.open(image)

    # if max_picture_width == MAX_FILE_WIDTH and max_picture_height == MAX_FILE_HEIGHT:
    #     img = resize_image_to_ratio(img, max_picture_width, max_picture_height)
    # else:
    img = resize_image_to_max_dimensions(img, max_picture_width, max_picture_height)

    image = compress_image(img)

    file_extension = '.jpg'
    new_filename = f"{prefix}-{instance.id}-{uuid.uuid4()}{file_extension}"
    image.name = new_filename

    image_file = InMemoryUploadedFile(image, 'image', image.name, 'image/jpeg', image.tell(), None)
    
    setattr(instance, image_field_name, image_file)
    instance.save()

    return image_file

def convert_image_to_jpg(img):
    output = BytesIO()
    img.convert('RGB').save(output, format='JPEG')
    output.seek(0)
    return output

def resize_image_to_max_dimensions(img, max_picture_width, max_picture_height):
    width, height = img.size
    ratio = min(max_picture_width / width, max_picture_height / height)
    
    if ratio < 1:
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return img

def compress_image(img):
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)
    return output
