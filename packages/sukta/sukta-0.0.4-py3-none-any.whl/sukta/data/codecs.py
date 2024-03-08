import imagecodecs
import numpy
from numcodecs.abc import Codec
from numcodecs.registry import get_codec, register_codec


def protective_squeeze(x: numpy.ndarray):
    """
    Squeeze dim only if it's not the last dim.
    Image dim expected to be *, H, W, C
    """
    img_shape = x.shape[-3:]
    if len(x.shape) > 3:
        n_imgs = numpy.prod(x.shape[:-3])
        if n_imgs > 1:
            img_shape = (-1,) + img_shape
    return x.reshape(img_shape)


class Jpeg2k(Codec):
    """JPEG 2000 codec for numcodecs."""

    codec_id = "imagecodecs_jpeg2k"

    def __init__(
        self,
        level=None,
        codecformat=None,
        colorspace=None,
        tile=None,
        reversible=None,
        bitspersample=None,
        resolutions=None,
        numthreads=None,
        verbose=0,
    ):
        self.level = level
        self.codecformat = codecformat
        self.colorspace = colorspace
        self.tile = None if tile is None else tuple(tile)
        self.reversible = reversible
        self.bitspersample = bitspersample
        self.resolutions = resolutions
        self.numthreads = numthreads
        self.verbose = verbose

    def encode(self, buf):
        buf = protective_squeeze(numpy.asarray(buf))
        return imagecodecs.jpeg2k_encode(
            buf,
            level=self.level,
            codecformat=self.codecformat,
            colorspace=self.colorspace,
            tile=self.tile,
            reversible=self.reversible,
            bitspersample=self.bitspersample,
            resolutions=self.resolutions,
            numthreads=self.numthreads,
            verbose=self.verbose,
        )

    def decode(self, buf, out=None):
        return imagecodecs.jpeg2k_decode(
            buf, verbose=self.verbose, numthreads=self.numthreads, out=out
        )


def register_codecs(codecs=None):
    """Register codecs in this module with numcodecs."""
    for name, cls in globals().items():
        if not hasattr(cls, "codec_id") or name == "Codec":
            continue
        if codecs is not None and cls.codec_id not in codecs:
            continue
        try:
            try:
                get_codec({"id": cls.codec_id})
            except TypeError:
                # registered, but failed
                pass
        except ValueError:
            # not registered yet
            pass
        register_codec(cls)
