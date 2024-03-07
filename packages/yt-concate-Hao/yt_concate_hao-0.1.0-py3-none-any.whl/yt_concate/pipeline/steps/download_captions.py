import os
import time
import yt_dlp
from threading import Thread
from webvtt import WebVTT

from .step import Step
from yt_concate.yt_logging import generate_logger


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = generate_logger()
        start = time.time()
        caption_list = []
        for yt in data:
            if utils.caption_file_exists(yt) and inputs['fast']:
                logger.info(f'Caption file exists for {yt.url}, skipping')
                continue
            else:
                caption_list.append(yt)

        threads = []
        threads_num = os.cpu_count()

        divide_c_list = [caption_list[i:len(caption_list):threads_num]for i in range(0, threads_num)]

        for i in range(threads_num):
            threads.append(Thread(target=self.download_caption, args=(divide_c_list[i], logger, )))
            threads[i].start()

        for i in range(os.cpu_count()):
            threads[i].join()

        end = time.time()
        logger.info('took', end - start, 'seconds')

        data = caption_list

        return data

    @staticmethod
    def download_caption(c_list, logger):
        for c_yt in c_list:
            url = c_yt.url
            ydl_opts = {
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'outtmpl': c_yt.caption_filepath,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    logger.info('Downloading caption for', c_yt.id)
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    logger.error(f"Error downloading subtitles: {e}")

            vtt_file_path = c_yt.caption_filepath + '.en.vtt'
            srt_file_path = c_yt.caption_filepath

            # 轉換 VTT 到 SRT
            if os.path.exists(vtt_file_path):
                vtt = WebVTT().read(vtt_file_path)
                with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                    for caption in vtt:
                        srt_file.write(f"{caption.start} --> {caption.end}\n{caption.text}\n")
                os.remove(vtt_file_path)  # 刪除原始的 VTT 檔案
            else:
                logger.info(f"VTT file not found at {vtt_file_path}")
