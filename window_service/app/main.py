from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  
from app import routers

import logging

logger = logging.getLogger('uvicorn')

origins = ["*"] 

app = FastAPI()
app.include_router(routers.router)


app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。

@app.get("/")
async def root():
    return {"message": "success"}

