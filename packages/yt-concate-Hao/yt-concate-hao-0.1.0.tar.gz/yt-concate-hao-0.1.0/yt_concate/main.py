import sys
import getopt
import logging
# sys.path.append('../') # CMD 讀不到 yt_concate
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils
from yt_logging import config_logger

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def opt_print(argv):
    print('python {} options'.format(argv[0]))
    print('options:')
    print('{:<3} {:<12} {}'.format('-c', '--channel', 'Channel id of the Youtube channel to download.'))
    print('{:<3} {:<12} {}'.format('-s', '--search', 'The words to search whether which the captions contain.'))
    print('{:<3} {:<12} {}'.format('-l', '--limit', 'A limit that the number of downloaded videos to merge.'))
    print('{:<3} {:<12} {}'.format('-f', '--fast', 'Whether to check if the files (including videos and captions)'))
    print('{:<15} {}'.format('', 'are already on the computer first.'))
    print('{:<3} {:<12} {}'.format('', '--cleanup', 'After the result file is created, delete the files created'))
    print('{:<15} {}'.format('', 'during the program execution, such as downloaded videos/subtitles, etc.'))


def main(argv):
    opt_argv = argv[1:]
    logging_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'cleanup': False,
        'fast': True,
        'level': logging.WARNING,
    }

    short_opts = 'hc:s:l:f:'
    long_opts = [
        'channel=',
        'search=',
        'limit=',
        'cleanup=',
        'fast=',
        'level=',
    ]

    try:
        opts, args = getopt.getopt(opt_argv, short_opts, long_opts)
    except getopt.GetoptError:
        opt_print(argv)
        sys.exit(2)
    for opt, arg in opts:
        try:
            if opt == 'h':
                opt_print(argv)
                sys.exit(0)
            elif opt == '--cleanup':
                inputs['cleanup'] = bool(arg)
            elif opt == '--level':
                if arg not in logging_levels:
                    continue
                inputs['level'] = f'logging.{arg}'
            elif opt in ('-c', '--channel'):
                inputs['channel_id'] = arg
            elif opt in ('-s', '--search'):
                inputs['search_word'] = arg
            elif opt in ('-l', '--limit'):
                inputs['limit'] = int(arg)
            elif opt in ('-f', '--fast'):
                inputs['fast'] = bool(arg)
        except ValueError as e:
            print(f'發生 ValueError: {e}')

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    config_logger(inputs['level'])
    p.run(inputs, utils)


if __name__ == '__main__':
    main(sys.argv)
