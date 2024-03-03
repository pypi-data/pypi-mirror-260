"""Main module.


TODO:

- [ ] get all info from media streams
- [x] extract ID3 metainfo to analyze format --> not relevant
- [x] extract rtp metainfo to analyze format
- [ ] specs for desired final format that allows:
  - [ ] convert just some streams and copy others
  - [ ] remove a stream according codec_tag_name, lang, etc
  - [ ] reduce BPS or Screen Size in some cases


"""

# library modules
# import asyncio
import os
import time
import pickle
import random
import re
import json

from pprint import pp

from boltons.dictutils import OrderedMultiDict as OMD
from boltons.iterutils import flatten, remap, default_enter, default_exit, default_visit

from glom import glom, Merge, T, Iter, A, S, Path, Spec, merge

# library partial
# from time import sleep


import ffmpeg

# local imports
# from .helpers import parse_uri
# ---------------------------------------------------------
# parallel processing
# ---------------------------------------------------------
from syncmodels.parallel import Parallel
from syncmodels.syncmodels import SyncModel

# ---------------------------------------------------------
# helpers
# ---------------------------------------------------------
from agptools.containers import walk
#import jmespath

# ---------------------------------------------------------
# models / mappers
# ---------------------------------------------------------
from .models import *
from . import mappers

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger

log = logger(__name__)

# subloger = logger(f'{__name__}.subloger')


# =========================================================
# extract
# =========================================================
class Xtract_0:
    def __init__(self, *include):
        self.include = include
        self._path_stack = []

        self._nodes = 0
        self._visit = 0

    def apply(self, subset):
        return remap(subset, visit=self.visit, enter=self.enter, exit=self.exit)

    def visit(self, path, key, value):
        # if re.match(r'codec_.*', str(key)):
        # return key, value
        # return False

        # if key == 'id':
        # return key, int(value, base=16)

        return key, value

    def enter(self, path, key, value):
        # value can be a container or single element
        if isinstance(value, dict):
            # entering in a node
            foo = 1

        # if isinstance(value, dict):
        # return OMD(), sorted(value.items())
        ret = default_enter(path, key, value)
        return ret

    def exit(self, path, key, old_parent, new_parent, new_items):
        if False:
            if 'codecs' in path:
                foo = 1

            try:
                codec_tag = old_parent.get('codec_tag', None)
                if codec_tag:
                    if codec_tag not in ('h264',):
                        new_items = [
                            (k, v) for k, v in new_items if re.match('codec_.*', str(k))
                        ]
                        foo = 1
            except Exception as why:
                pass

        ret = default_exit(path, key, old_parent, new_parent, new_items)
        # if isinstance(ret, list):
        # ret.sort()
        return ret


class TranslateMarks:
    SEP = r'@'
    ORG = '/'

    def __call__(self, subset):
        return remap(subset, visit=self._visit)

    def revert(self, value: str):
        def f(x):
            try:
                x = int(x)
            except Exception:
                pass
            return x

        value = tuple([f(x) for x in value.split(self.SEP)])
        return value

    def _visit(self, path, key, value):
        if isinstance(key, str):
            key = r'{}'.format(self.SEP).join(key.split(self.ORG))

        if isinstance(value, str):
            value = r'{}'.format(self.SEP).join(value.split(self.ORG))

        return key, value


class Xpecs(dict):
    """Helper class to check Deep/Rebuil seearches"""

    NEEDED_KEYS = set(['root', 'match', 'gather'])

    def __init__(self, *iterable, **kwargs):
        super().__init__(*iterable, **kwargs)
        self.check()

    def check(self):
        # check all needed keys are present
        for block, spec in self.items():
            assert not self.NEEDED_KEYS.symmetric_difference(spec), "mssing keys"
            if isinstance(spec['match'][0], str):
                # fix, need to be a list of list matches
                spec['match'] = [spec['match']]
            assert spec['gather'], "must collect something"


class Xtract:
    SEP = r'@'

    def __init__(self, specs):
        self.result = {}
        self.target = None
        self.match = set()

        self.trans = TranslateMarks()

        self.specs = specs
        self._specs = self.trans(specs)

    def apply(self, target):
        self.target = target
        self.match = set()

        # def recover(k, parent):
        # result = T
        # for key in k[: len(parent.split(self.SEP))]:
        # result = result[key]
        # return result

        ctx = {}

        def expand(exp: str):
            if isinstance(exp, tuple):
                exp = self.SEP.join([str(_) for _ in exp])
            try:
                exp = exp.format_map(ctx)
            except Exception as why:
                pass
            return exp

        def unroll(spec):
            value = self.target
            org_spec = spec
            try:
                if isinstance(spec, str):
                    spec = self.trans.revert(spec)
                for x in spec:
                    value = value[x]
            except Exception:
                return org_spec

            return value

        def check(expression: str):
            # '1.codecs.2.codec_name != h264|acc'

            parts = re.split('\s*(==|\!=)\s*', expression)
            parts = [expand(exp) for exp in parts]

            spec, eq, pattern = parts
            spec = self.trans.revert(spec)

            value = unroll(spec)
            m = re.match(pattern, str(value))
            if (m is None) ^ (eq in ('==',)):
                ctx[spec[-1]] = value
                return True
            return False

        specs = self._specs
        for block, _specs in specs.items():
            root_exp = _specs['root']
            match_exp = _specs['match']
            gather_exp = _specs['gather']

            for key, value in walk(target):
                # print(f"??? {key}: {value}")
                key = expand(key)
                value = expand(value)
                if ctx.get('root'):
                    for mexpr in match_exp:
                        result = [check(expression) for expression in mexpr]
                        if all(result):
                            item = {
                                k.format_map(ctx): unroll(v.format_map(ctx))
                                for k, v in gather_exp.items()
                            }
                            self.result.setdefault(ctx['root'], {}).update(item)
                            foo = 1
                    ctx.clear()
                else:
                    m = re.match(root_exp, key)
                    if m:
                        d = m.groupdict()
                        ctx.update(d)
                        foo = 1

        return self.result


# =========================================================
# pytranscoding
# =========================================================
MAP = {
    '(': '.',
    ')': '.',
    '[': '.',
    ']': '.',
    '-': '.',
    '!': '.',
    ':': '.',
    'ñ': 'n',
}
TRANS = str.maketrans(MAP)

REPL = {
    '..': '.',
    ' ': '.',
    ',': '.',
    ';': '.',
    '.eac3.': '.',
    '.cd1.': '.',
    '.cd2.': '.',
    '.x264.': '.',
    '.web.': '.',
    '.dl.': '.',
    '.spanish.': '.',
    '.english.': '.',
    '.subs.': '.',
    '.by': '.',
    '.1080p.': '.',
    '_1': '',
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',
}


def simplify_filename(path: str):
    dirname, basename = os.path.split(path)
    basename = basename.lower()

    # replace weird chars
    basename = basename.translate(TRANS)

    # replace tokens

    last = None
    while last != basename:
        last = basename
        for old, new in REPL.items():
            basename = basename.replace(old, new)

    path = os.path.join(dirname, basename)

    return path


CODECS = (
    # erase una vez
    ('h264', '0x0000'),
    # honeylips ph606af5c940e26.mp4
    ('h264', '0x001b'),
    # lick 64ff82d22f373
    # ffmpeg -i input.mkv -vcodec libx264 -acodec aac output.mp4
    ('h264', '0x31637661'),
    # Cathy Avril
    ('h264', '0x34363248'),
    # Billions
    ('hevc', '0x0000'),
    # Incendies
    ('mjpeg', '0x0000'),
    # brocoli, need conversion
    ('mpeg4', '0x001b'),
    # Enano Rojo
    ('mpeg4', '0x30355844'),
    # 'mpeg4'  'Erase.una.vez' need conversion
    ('mpeg4', '0x44495658'),
    # Sally, Jennifer
    ('mpeg4', '0x7634706d'),
    # Enano Rojo
    ('mpeg4', '0x78766964'),
    # Sharon Lee
    ('msmpeg4v2', '0x3234504d'),
    # Red_Dwarf
    ('msmpeg4v3', '0x33564944'),
    # audio codecs
    ('aac', '0x6134706d'),
)


class Transcoder(SyncModel):
    ERROR = 'error'
    MEDIA = 'media'
    MAPPERS = {
        'video': mappers.VideCodecInfo,
        'audio': mappers.AudioCodecInfo,
        'data': mappers.CodecInfo,
        'subtitle': mappers.AudioCodecInfo,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Model()

    def _bootstrap(self):
        yield self._sync_explorer, [], {}

    def _sync_explorer(self):
        for name, top in self.cfg['folders'].items():
            self._add_task(self._sync_explore_folder, top=top)

    def _sync_explore_folder_old(self, top):
        pattern = r"(?P<file>(?P<basename>.*?)(?P<ext>\.(avi|mkv|mp4)*))$"
        for root, folders, names in os.walk(top):
            for name in names:
                # if 'Bajo.el.manto' not in name:
                # continue
                path = os.path.join(root, name)
                m = re.match(pattern, path)
                if m:
                    self._add_task(self._analyze_media_file, path=path)

    def _sync_explore_folder(self, top):
        candidates = []
        pattern = r"(?P<file>(?P<basename>.*?)(?P<ext>\.(avi|mkv|mp4)*))$"
        for root, folders, names in os.walk(top):
            for name in names:
                # if 'Bajo.el.manto' not in name:
                # continue
                path = os.path.join(root, name)
                m = re.match(pattern, path)
                if m:
                    candidates.append(path)

        random.shuffle(candidates)
        for path in candidates:
            self._add_task(self._analyze_media_file, path=path)

    def _analyze_media_file(self, path):
        # log.info(f"Analyze: {path}")
        # MEDIA = self.model.setdefault(self.MEDIA, {})
        MEDIA = self.model.media
        ERROR = self.model.error

        current = MEDIA.get(path)
        if current and not self._overwrite:
            # TODO: check last update
            if True:
                return

        try:
            info = ffmpeg.probe(path)
        except ffmpeg.Error:
            # error = self.model.setdefault(self.ERROR, {})
            ERROR[path] = datetime.utcnow()
            return
        media = mappers.MediaFile.pydantic(info['format'])

        for data in info['streams']:
            type_ = data['codec_type']
            codec = self.new(type_, data)
            media.codecs.append(codec)

        # add to media
        MEDIA[path] = media

        # try to remove from error (just-in-case)
        ERROR.pop(path, None)

    def apply_old(self):
        log.info(f"Loading model from disk ...")
        self.load_model()
        log.info(f"Apply GAPs ...")

        data = self.model.dict(exclude='error')

        subset = {}
        for i, (k, v) in enumerate(data['media'].items()):
            if 'Star' not in str(k):
                continue
            subset[k] = v
            if len(subset) >= 1:
                break

        invented = {
            'fix-video': {
                'root': '(?P<path>(?P<root>.*?)/codecs/(?P<index>\d+))$',
                'match': [
                    # [
                    #'{path}/codec_name != h264|aac',
                    #'{path}/codec_type == video|audio',
                    # ],
                    [
                        '{path}/codec_name != h264',
                        '{path}/codec_type == video',
                    ],
                    [
                        '{path}/codec_name != aac',
                        '{path}/codec_type == audio',
                    ],
                ],
                'gather': {
                    'path': '{root}/path',
                    '{codec_type}': '{codec_name}',
                },
            }
        }
        spec = Xpecs(invented)

        X = Xtract(spec)

        subset = data['media']
        result = X.apply(subset)
        temp = self.cfg['temp']

        for path, info in result.items():
            dirname, filename = os.path.splitext(path)

            _path = simplify_filename(path)
            _dirname, _filename = os.path.split(_path)
            _basename, ext = os.path.splitext(_filename)

            dirname, filename = os.path.split(_path)

            # _basename = f"/tmp/{os.path.basename(path)}"
            # _ext = ext
            # _basename = '/tmp/output'
            _ext = '.mkv'
            # _ext = '.mp4'
            # _temp_path = os.path.join(temp, _basename)
            _temp_path = f"{temp}/{_basename}.new{_ext}"

            # info2 = ffmpeg.probe(_path)

            # analyze needs
            extra = {
                #'t': 120,
                'map': 0,
            }

            # analize streams
            try:
                info1 = ffmpeg.probe(path)
            except Exception as why:
                log.error(why)
                continue
            # level = info1['streams'][0]['level']
            for stream in info1['streams']:
                if stream['codec_type'] in ('video',):
                    if stream['codec_name'] not in ('h264',):
                        extra['vcodec'] = 'libx264'

                if stream['codec_type'] in ('audio',):
                    if stream['codec_name'] not in ('aac',):
                        extra['acodec'] = 'aac'

                if stream['codec_type'] in ('subtitle',):
                    if stream['codec_name'] not in ('subrip', 'srt', 'ass'):  # subrip
                        extra['scodec'] = 'srt'

            chain = (
                ffmpeg.input(path)
                .output(_temp_path, **extra)
                .overwrite_output()
                # .overwrite_output()
                # .overwrite_output()
                # .overwrite_output()
            )

            cmd = chain.compile()

            debug = '\n '.join(cmd)
            debug = '  '.join(cmd)

            log.info(f">> {debug}")

            chain.run()
            _path = f"{dirname}/{_basename}{_ext}"
            try:
                os.renames(_temp_path, _path)
                os.unlink(path)
            except Exception as why:
                log.error(why)
            foo = 1
            # break
        foo = 1

    def apply(self, pattern=[], force=False, shuffle=False, dryrun=False):
        log.info(f"Loading model from disk ...")
        self.load_model()
        log.info(f"Apply GAPs ...")

        data = self.model.dict(exclude='error')
        
        subset = {}
        for i, (k, v) in enumerate(data['media'].items()):
            subset[k] = v
            if len(subset) >= 1:
                break

        invented = {
            'fix-video': {
                'root': '(?P<path>(?P<root>.*?)/codecs/(?P<index>\d+))$',
                'match': [
                    # [
                    #'{path}/codec_name != h264|aac',
                    #'{path}/codec_type == video|audio',
                    # ],
                    [
                        '{path}/codec_name != h264',
                        '{path}/codec_type == video',
                    ],
                    [
                        '{path}/codec_name != aac',
                        '{path}/codec_type == audio',
                    ],
                ],
                'gather': {
                    'path': '{root}/path',
                    '{codec_type}': '{codec_name}',
                },
            }
        }
        spec = Xpecs(invented)

        X = Xtract(spec)

        subset = data['media']
        result = X.apply(subset)

        def convert(path, force=False, dryrun=False):
            # print(path)
            dirname, filename = os.path.splitext(path)

            _path = simplify_filename(path)
            _dirname, _filename = os.path.split(_path)
            _basename, ext = os.path.splitext(_filename)

            dirname, filename = os.path.split(_path)

            # _basename = f"/tmp/{os.path.basename(path)}"
            # _ext = ext
            # _basename = '/tmp/output'
            _ext = '.mkv'
            # _ext = '.mp4'
            # _temp_path = os.path.join(temp, _basename)
            _temp_path = f"{temp}/{_basename}.new{_ext}"
            _path = f"{dirname}/{_basename}{_ext}"
            if path != _path:
                force = True
            elif force == False:
                return

            # info2 = ffmpeg.probe(_path)

            # analyze needs
            extra = {
                #'t': 120,
                #'map': 0,
                #'vcodec': 'libx264', 
                #'acodec': 'aac',
                'cpucount': 1,
                'threads': 1, 
                'loglevel': 'info',
                #'hide_banner': '',
            }
            vcodec = {}
            acodec = {}
            scodec = {}
            # analize streams
            try:
                info1 = ffmpeg.probe(path)
            except Exception as why:
                log.error(why)
                return

            # level = info1['streams'][0]['level']
            # select just video, audo and subtitles that are compatible
            for stream in info1['streams']:
                if stream['codec_type'] in ('video',):
                    if stream['codec_name'] not in ('h264',):
                        pass
                    vcodec[f'codec:v:{len(vcodec)}'] = 'libx264'
                    

                if stream['codec_type'] in ('audio',):
                    if stream['codec_name'] not in ('aac',):
                        pass
                    acodec[f'codec:a:{len(acodec)}'] = 'aac'
                    
                if stream['codec_type'] in ('subtitle',):
                    if stream['codec_name'] in ('subrip', 'srt', 'ass'):  # subrip
                        scodec[f'codec:s:{len(scodec)}'] = stream['codec_name']
                    else:
                        print(f"Ignoring: {stream['codec_type']}: {stream['codec_name']}")
                        
                    
            if not (vcodec or acodec or scodec):
                return
            
            if dryrun:
                return
            
            chain = (
                ffmpeg.input(path)
                .output(
                    _temp_path,
                    **extra,
                    **vcodec,
                    **acodec,
                    **scodec, 
                    
                )
                .overwrite_output()
                # .overwrite_output()
                # .overwrite_output()
                # .overwrite_output()
            )

            cmd = chain.compile()

            debug = '\n '.join(cmd)
            debug = '  '.join(cmd)

            columns, lines = os.get_terminal_size()
            columns = max(columns-40, 40)
            log.info(f"-" * columns)
            log.info(f">> {debug}")
            #log.info(f"{pp(info1)}")
            if info1:
                log.info(f"Duration: {info1['streams'][0].get('duration', -1)} secs")
            log.info(f"-" * columns)
            time.sleep(5)

            try:
                chain.run()
                try:
                    os.renames(_temp_path, _path)
                    os.unlink(path)
                    pass
                except Exception as why:
                    log.error(why)
            except Exception as why:
                log.error(why)
            foo = 1

        temp = self.cfg['temp']
        i = 0
        candidates = list()
        for name, top in self.cfg['folders'].items():
            regpex= r"(?P<file>(?P<basename>.*?)(?P<ext>\.(avi|mkv|mp4)*))$"
            for root, folders, names in os.walk(top):
                for name in names:
                    path = os.path.join(root, name)
                    
                    for patt in pattern:
                        if re.search(patt, path, re.I|re.DOTALL):
                            break
                    else:
                        continue
                                        
                    m = re.match(regpex, path)
                    if m:
                        i += 1
                        candidates.append(path)
                        
        if shuffle:
            random.shuffle(candidates)
            
        N = len(candidates)        
        for i, path in enumerate(candidates):
            log.info(f"[{i + 1}/{N}]: {path}")
            convert(path, force, dryrun)

            # break
        foo = 1


if False:
    from ffmpeg import input, output

    input_video = 'input_video.mp4'
    output_video = 'output_video.mp4'
    max_resolution = '1920x1080'  # Set your desired maximum resolution here

    ffmpeg_process = (
        input(input_video)
        .output(
            output_video,
            c='copy',
            vf=f'scale=w=min(iw,{max_resolution}):h=min(ih,{max_resolution})',
        )
        .run()
    )
