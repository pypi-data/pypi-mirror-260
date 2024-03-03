from syncmodels.mapper import *
from . import models

# NOTE:
# if use default only_defined=False
# we only need to define mappers when attribute name changes


class File(Mapper):
    PYDANTIC = models.File

    filename = 'path', STRIP
    file = 'path', STRIP


class CodecInfo(Mapper):
    PYDANTIC = models.CodecInfo

    bit_rate = I, I
    codec_name = I, STRIP
    codec_long_name = I, STRIP

    codec_tag = I, I
    codec_tag_string = I, STRIP
    codec_type = I, STRIP
    duration = I, I


class MediaFile(File):
    PYDANTIC = models.MediaFile
    codecs = I, I


class AudioCodecInfo(CodecInfo):
    PYDANTIC = models.AudioCodecInfo
    pass


class SubtitleCodecInfo(CodecInfo):
    PYDANTIC = models.SubtitleCodecInfo
    pass


class VideCodecInfo(CodecInfo):
    PYDANTIC = models.VideoCodecInfo
    pass
