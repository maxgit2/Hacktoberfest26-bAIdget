from io import BytesIO

import pytest
from PIL import Image

from app.imaging.image import UnsupportedImageTypeError, prepare_image


def image_bytes(
    *, size: tuple[int, int] = (32, 24), format: str = "JPEG", exif=None
) -> bytes:
    output = BytesIO()
    options = {} if exif is None else {"exif": exif}
    Image.new("RGB", size, "white").save(output, format=format, **options)
    return output.getvalue()


async def test_image_is_resized_reencoded_and_exif_is_removed():
    exif = Image.Exif()
    exif[0x8825] = {
        1: "N",
        2: (41.0, 54.0, 0.0),
        3: "E",
        4: (12.0, 30.0, 0.0),
    }

    prepared = await prepare_image(
        image_bytes(size=(3000, 1500), format="JPEG", exif=exif)
    )

    with Image.open(BytesIO(prepared)) as image:
        assert image.format == "JPEG"
        assert image.size == (2048, 1024)
        assert len(image.getexif()) == 0


async def test_transparent_png_is_flattened_to_jpeg():
    source = BytesIO()
    Image.new("RGBA", (20, 20), (255, 0, 0, 0)).save(source, format="PNG")

    prepared = await prepare_image(source.getvalue())

    with Image.open(BytesIO(prepared)) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"


async def test_invalid_and_excessive_pixel_images_are_rejected(monkeypatch):
    with pytest.raises(UnsupportedImageTypeError):
        await prepare_image(b"not an image")

    source = image_bytes(size=(11, 10))
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 100)
    with pytest.raises(UnsupportedImageTypeError):
        await prepare_image(source)
