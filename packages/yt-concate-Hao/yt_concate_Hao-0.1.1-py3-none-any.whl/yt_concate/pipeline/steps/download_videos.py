import os
import yt_dlp
from threading import Thread

from .step import Step
from yt_concate.yt_logging import generate_logger


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = generate_logger()
        yt_set = set([found.yt for found in data])
        logger.info('Videos to download = ', len(yt_set))
        video_list = []

        for yt in yt_set:
            if utils.video_file_exists(yt) and inputs['fast']:
                logger.info(f'Video file exists for {yt.url}, skipping')
                continue
            else:
                video_list.append(yt)

        threads = []
        threads_num = os.cpu_count()

        divide_v_list = [video_list[i:len(video_list):threads_num] for i in range(0, threads_num)]

        for i in range(os.cpu_count()):
            threads.append(Thread(target=self.download_video, args=(divide_v_list[i], logger, )))
            threads[i].start()

        for i in range(os.cpu_count()):
            threads[i].join()

        return data

    @staticmethod
    def download_video(v_list, logger):
        for yt in v_list:
            url = yt.url
            ydl_opts = {
                'outtmpl': yt.video_filepath,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    logger.info('Downloading video for', url)
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    logger.error(f"Error downloading video: {e}")
