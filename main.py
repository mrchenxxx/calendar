import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from lunarcalendar import Converter, Lunar, Solar
from datetime import datetime
from lark import main
from convert_date import convert_date

app = FastAPI()


class DateRequest(BaseModel):
    date: str
    canl: str
    record_id: str


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

