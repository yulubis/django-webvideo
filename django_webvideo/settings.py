# coding: utf-8
from django.conf import settings


DEFAULT_SETTINGS = {
    'upload_to': 'videos',
    'convert_to': 'videos/converted',
    'screens_to': 'videos/screens',
    'ffmpeg': {
        'binary': 'ffmpeg',
        'call_h264': "{ffmpeg} -y -i {infile} -acodec libmp3lame -ar 48000 -ab 128k -ac 2 -vcodec libx264 "
                     "-cmp 256 -subq 7 -trellis 1 -refs 5 -coder 0 -me_range 16 -keyint_min 25 -sc_threshold 40 "
                     "-i_qfactor 0.71 -bt 1200k -maxrate 1200k -bufsize 1200k -rc_eq 'blurCplx^(1-qComp)' "
                     "-qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -level 30 -r 30 -g 90 {outfile}",
        'call_ogv': '{ffmpeg} -i {infile} -b 1200k -vcodec libtheora -acodec libvorbis -ab 160000 {outfile}',
    },
    'redis': {
        'connection': {
            'db': 0,
            'host': 'localhost',
            'port': 6379,
        },
        'eager': False,  # If True, Tasks are not queued, but executed directly. Use for testing purposes only!
        'queue_prefix': 'webvideo',  # django_webvideo will prefix all (RQ-)Queues with this prefix.
        'timeout': 600,
    }
}


def _get_setting(setting, key, *subkeys):
    if len(subkeys) > 0:
        while setting is not None and isinstance(setting, dict) and len(subkeys) > 0:
            setting = setting.get(key)
            key = subkeys[0]
            subkeys = subkeys[1:]
        try:
            return setting.get(key)
        except AttributeError:
            return None
    else:
        return setting.get(key)


def get_setting(key, *subkeys):
    value = _get_setting(getattr(settings, 'DJANGO_WEBVIDEO_SETTINGS'), key, *subkeys)
    if value is None:
        return _get_setting(DEFAULT_SETTINGS, key, *subkeys)
    else:
        return value


def get_queue_name():
    return "{0}:convert".format(get_setting('redis', 'queue_prefix'))