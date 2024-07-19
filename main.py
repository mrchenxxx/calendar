import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
import json
from pydantic import BaseModel
from datetime import datetime
from lunarcalendar import Converter, Lunar
from datetime import datetime
from lark import main
from convert_date import convert_date

import os

os.getenv(".env")

load_dotenv()


app = FastAPI()


class VerifyFieldMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            body = await request.body()
            data = json.loads(body)
            if data.get("SECRET_KEY") != os.getenv("SECRET_KEY"):
                raise HTTPException(
                    status_code=400, detail="Invalid value for 'SECRET_KEY'"
                )
        response = await call_next(request)
        return response


app.add_middleware(VerifyFieldMiddleware)


class DateRequest(BaseModel):
    """
    BaseModel参数
    :param date: 输入的下次提醒日期
    :param canl: 输入的阴历/阳历类型
    :param record_id: 输入的记录id
    """

    date: str
    canl: str
    record_id: str
    SECRET_KEY: str


def lunar_to_solar(lunar_date_str):
    lunar_date = datetime.strptime(lunar_date_str, '%Y/%m/%d')
    lunar = Lunar(lunar_date.year, lunar_date.month, lunar_date.day)
    solar = Converter.Lunar2Solar(lunar)
    return datetime(solar.year, solar.month, solar.day)


@app.post("/convert-date")
async def convert_date_main(request: DateRequest):

    date_obj = await convert_date(request.date, request.canl)

    # 将datetime对象转换为时间戳（以秒为单位）
    timestamp_seconds = int(date_obj.timestamp())

    # 将时间戳转换为毫秒
    timestamp_milliseconds = timestamp_seconds * 1000

    await asyncio.create_task(main(request.record_id, timestamp_milliseconds))

    return {"new_date": timestamp_milliseconds}
