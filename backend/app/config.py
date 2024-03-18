import os

HTML_IMAGE_DEFAULT_PATH = "./images" # 图片文件爬虫路径
VIDEO_FILE_PATH = "videos/raw_videos" # 原始视频存放路径
VIDEO_EXTRACT_PATH = "videos/video_frames" # 抽帧存储文件夹路径
VIDEO_KEEP_RECENT_DAYS = 1 # 保留最近几天的视频文件
VIDEO_REMOVE_INTERVAL = 30 # 多少分钟调度清除任务一次
VIDEO_CALLBACK_URL = "" # 视屏处理结果回调地址
KPS = 1 # 每秒多少帧
USE_GPU = False # 是否使用GPU
IMAGE_PATH = "../images"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'

mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_db = os.getenv("MYSQL_DB")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:3306/{mysql_db}"


def create_tmp_folders():
    
    if not os.path.exists(VIDEO_FILE_PATH):
        os.makedirs(VIDEO_FILE_PATH)

    if not os.path.exists(VIDEO_EXTRACT_PATH):
        os.makedirs(VIDEO_EXTRACT_PATH)
        
    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)