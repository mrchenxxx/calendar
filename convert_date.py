import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist


def is_valid_date(year, month, day):
    try:
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False


async def convert_date(date_str, canl):
    year, month, day = map(int, date_str.split('/'))

    now = datetime.datetime.now()

    if canl == "阴历":
        try:
            lunar_date = Lunar(year, month, day)
            solar_date = Converter.Lunar2Solar(lunar_date)
        except DateNotExist:
            raise ValueError("提供的阴历日期不存在，请检查日期是否正确。")

        # 如果转换后的日期早于当前时间，则转换为下一年的日期
        while (
            datetime.datetime(solar_date.year, solar_date.month, solar_date.day) < now
        ):
            year += 1
            try:
                lunar_date = Lunar(year, month, day)
                solar_date = Converter.Lunar2Solar(lunar_date)
            except DateNotExist:
                raise ValueError("提供的阴历日期在下一年不存在，请检查日期是否正确。")

        return datetime.datetime(solar_date.year, solar_date.month, solar_date.day)

    elif canl == "阳历":
        solar_date = datetime.datetime(year, month, day)
        # 如果给定的阳历日期早于当前时间，则转换为下一年的日期
        while solar_date < now:
            year += 1
            if is_valid_date(year, month, day):
                solar_date = datetime.datetime(year, month, day)
            else:
                # Handle invalid date, e.g., 2/29 in a non-leap year
                if month == 2 and day == 29:
                    month = 3
                    day = 1
                solar_date = datetime.datetime(year, month, day)
        return solar_date

    else:
        raise ValueError("无效的日期类型")


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(convert_date("2024/02/29", "阳历"))
    print(res)
