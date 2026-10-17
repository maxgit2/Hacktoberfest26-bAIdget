import warnings
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

MAX_LONG_SIDE = 2048
SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


class UnsupportedImageTypeError(ValueError):
    pass


def _prepare_image(image_bytes: bytes) -> bytes:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(image_bytes)) as source:
                if source.format not in SUPPORTED_FORMATS:
                    raise UnsupportedImageTypeError
                if (
                    Image.MAX_IMAGE_PIXELS is not None
                    and source.width * source.height > Image.MAX_IMAGE_PIXELS
                ):
                    raise UnsupportedImageTypeError

                image = ImageOps.exif_transpose(source)
                if image.mode in {"RGBA", "LA"} or (
                    image.mode == "P" and "transparency" in image.info
                ):
                    rgba = image.convert("RGBA")
                    background = Image.new("RGB", rgba.size, "white")
                    background.paste(rgba, mask=rgba.getchannel("A"))
                    image = background
                else:
                    image = image.convert("RGB")
                image.thumbnail(
                    (MAX_LONG_SIDE, MAX_LONG_SIDE), Image.Resampling.LANCZOS
                )

                output = BytesIO()
                image.save(output, format="JPEG", quality=85)
                return output.getvalue()
    except UnsupportedImageTypeError:
        raise
    except (
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        OSError,
        UnidentifiedImageError,
        ValueError,
    ) as exc:
        raise UnsupportedImageTypeError from exc


async def prepare_image(image_bytes: bytes) -> bytes:
    return await run_in_threadpool(_prepare_image, image_bytes)
