import logging

from app import routers
from app.auth import authentication
from app.auth.oauth2 import oauth2_scheme
from app.config import create_tmp_folders
from app.database import create_mysql_database_if_not_exists, engine
from app.models import Base
from app.utils import remove_file
from app.video_process import process_next_video
from app.config import VIDEO_REMOVE_INTERVAL
from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from apscheduler.schedulers.background import BackgroundScheduler
from starlette.middleware.cors import CORSMiddleware
from threading import Thread


logger = logging.getLogger('uvicorn')

origins = ["*"] 

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。


app.include_router(authentication.router)
app.include_router(routers.image.router)
app.include_router(routers.text.router)
app.include_router(routers.user.router)
app.include_router(routers.anomaly.router)
app.include_router(routers.videos.router)


@app.on_event("startup")
def init_project():

    # create database and folders
    create_mysql_database_if_not_exists()
    create_tmp_folders()

    # create all tables
    Base.metadata.create_all(bind=engine)
    
    # start video processing thread

    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_file,'interval',
                      minutes=VIDEO_REMOVE_INTERVAL)
    scheduler.start()
    
    logger.info("Start clearnup task successfully")
    consumer = Thread(target=process_next_video)
    consumer.start()

@app.get("/")
async def root():
    return {"message": "success"}

add_pagination(app)




