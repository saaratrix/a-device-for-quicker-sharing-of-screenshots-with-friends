import os
from typing import TypedDict, Literal, TYPE_CHECKING
from PIL import Image
from .file_upload_exception import FileUploadException
from .file_utility import FileUtility

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage

class CropCoordinates(TypedDict):
    x: int
    y: int


class CropSize(TypedDict):
    x: int
    y: int
    width: int
    height: int


class CropOptions(TypedDict):
    start: CropCoordinates
    size: CropSize


class FileTransformationOptions(TypedDict, total=False):
    rotation: Literal[0, 90, 180, 270]
    size: CropSize


class FileTransformation:

    @staticmethod
    def try_transform(file: 'FileStorage', transformation_options: FileTransformationOptions | None, upload_path: str) -> None:
        """
       Will attempt to transform the file based on the transformation options and finally save the file.
       """
        if transformation_options is None:
            return file.save(upload_path)

        file_type = FileTransformation.get_file_type(upload_path)
        transformed = False
        if file_type == 'image':
            transformed = FileTransformation.transform_image(file, transformation_options, upload_path)

        if transformed is False:
            file.save(upload_path)

        return None

    @staticmethod
    def get_file_type(filename):
        base, ext = os.path.splitext(filename)
        if ext.lower() in FileUtility.IMAGE_EXTENSIONS:
            return "image"

        return "unknown"

    @staticmethod
    def transform_image(file: 'FileStorage', transformation_options: FileTransformationOptions | None, upload_path: str) -> bool:
        img = None

        rotation = transformation_options.get('rotation')
        if rotation is not None and rotation != 0:
            try:
                # We flip the rotation because of CSS vs Pillow rotations.
                # 90 deg in CSS is -90 for Pillow.
                rotation = -rotation % 360
                # Pillow crashes on negative rotation.
                if rotation < 0:
                    rotation = 360 + rotation
                img = img or Image.open(file)
                img = img.rotate(rotation, expand=True)
            except Exception as e:
                raise FileUploadException(e, 'Failed to rotate image.')

        crop = transformation_options.get('crop')
        if crop is not None:
            x = crop['x']
            y = crop['y']
            width = crop['width']
            height = crop['height']
            if x >= 0 and y >= 0 and width > 0 and height > 0:
                try:
                    img = img or Image.open(file)
                    right = max(x + width, img.width)
                    bottom = max(y + height, img.height)
                    img = img.crop((x, y, right, bottom))
                except Exception as e:
                    raise FileUploadException(e, 'Failed to crop image.')

        if img is not None:
            try:
                img.save(upload_path)
                return True
            except Exception as e:
                raise FileUploadException(e, 'Failed to save transformed image.')

        return False

    @staticmethod
    def try_rotate():
        pass




