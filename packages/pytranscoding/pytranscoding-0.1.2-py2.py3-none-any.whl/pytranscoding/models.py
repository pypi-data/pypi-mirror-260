# 3rd party libraries

from syncmodels.model import BaseModel
from syncmodels.mapper import *

from typing import Union


class File(BaseModel):
    path: str = None
    tags: dict = {}


class CodecInfo(BaseModel):
    avg_frame_rate: str = None
    bit_rate: int = None

    codec_long_name: str = None
    codec_name: str = None
    codec_tag: str = None
    codec_tag_string: str = None
    codec_type: str = None

    # disposition: dict = {}  # TODO: karaoke, metadata, ..., necessary?

    duration: float = None
    duration_ts: int = None
    extradata_size: int = None
    id: str = None
    index: int = None
    nb_frames: int = None
    profile: str = None

    r_frame_rate: str = None

    start_pts: float = None
    start_time: float = None
    tags: dict = {}
    time_base: str = None


class VideoCodecInfo(CodecInfo):
    bits_per_raw_sample: int = 0

    chroma_location: str = None
    closed_captions: int = 0
    # H:W
    coded_height: int = 0  # TODO: necessary?
    coded_width: int = 0  # TODO: necessary?
    # color
    color_primaries: str = None
    color_range: str = None
    color_space: str = None
    color_transfer: str = None
    # display

    display_aspect_ratio: str = None

    field_order: str = None  # TODO: necessary?
    film_grain: int = 0  # TODO: necessary?

    has_b_frames: int = 0
    height: int = None
    is_avc: bool = False

    level: int = 0  # TODO: necessary?
    nal_length_size: int = 0  # TODO: necessary?

    pix_fmt: str = None
    profile: str = None
    refs: int = 0
    sample_aspect_ratio: str = None

    time_base: str = None

    width: int = None


class AudioCodecInfo(CodecInfo):
    bits_per_sample: int = 0

    channel_layout: str = None
    channels: int = None
    sample_fmt: str = None
    sample_rate: int = None


class SubtitleCodecInfo(CodecInfo):
    start_pts: int = 0


class MediaFile(File):
    duration: float = None
    codecs: List[Union[CodecInfo, AudioCodecInfo, VideoCodecInfo]] = []
    # codecs: Dict[str, [AudioCodecInfo | VideoCodecInfo]] = {}


class Model(BaseModel):
    media: Dict[str, MediaFile] = {}
    error: Dict[str, datetime] = {}
