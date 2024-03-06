# utilities
import os

from yt_concate.settings import DOWNLOADS_DIR
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import CAPTIONS_DIR
from yt_concate.settings import OUTPUTS_DIR
from yt_concate.yt_logging import generate_logger


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def create_dirs():
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(CAPTIONS_DIR, exist_ok=True)
        os.makedirs(OUTPUTS_DIR, exist_ok=True)

    @staticmethod
    def get_video_list_filepath(channel_id):
        return os.path.join(DOWNLOADS_DIR, channel_id + '.txt')

    def video_list_file_exists(self, channel_id):
        filepath = self.get_video_list_filepath(channel_id)
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    @staticmethod
    def caption_file_exists(yt):
        filepath = yt.caption_filepath
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    @staticmethod
    def video_file_exists(yt):
        filepath = yt.video_filepath
        return os.path.exists(filepath) and os.path.getsize(filepath) > 0

    @staticmethod
    def get_output_filepath(channel_id, search_word):
        filename = channel_id + '_' + search_word + '.mp4'
        return os.path.join(OUTPUTS_DIR, filename)

    @staticmethod
    def delete_files_in_directory(directory):
        logger = generate_logger()
        try:
            # 確保目錄存在
            if os.path.exists(directory):
                # 遍歷目錄中的所有文件
                for file_name in os.listdir(directory):
                    file_path = os.path.join(directory, file_name)

                    # 檢查文件是否存在並且是否是文件（不是子目錄）
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logger.info(f"文件 '{file_path}' 已成功刪除。")
                    else:
                        logger.info(f"跳過目錄 '{file_path}'。")

                logger.info(f"目錄 '{directory}' 下的所有文件已成功刪除。")
            else:
                logger.info(f"目錄 '{directory}' 不存在。")
        except Exception as e:
            logger.error(f"刪除目錄 '{directory}' 下的文件時發生錯誤: {e}")

    def delete_dirs(self):
        self.delete_files_in_directory(CAPTIONS_DIR)
        self.delete_files_in_directory(VIDEOS_DIR)
        self.delete_files_in_directory(DOWNLOADS_DIR)
