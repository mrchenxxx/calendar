from dotenv import load_dotenv
import requests
import json
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
import os

os.getenv(".env")

load_dotenv()


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps(
        {
            "app_id": os.getenv("APP_ID"),
            "app_secret": os.getenv("APP_SECRET"),
        }
    )
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["tenant_access_token"]


async def main(record_id, timestamp_milliseconds):

    token = get_token()

    client = (
        lark.Client.builder()
        .enable_set_token(True)
        .log_level(lark.LogLevel.DEBUG)
        .build()
    )

    # 构造请求对象
    request: UpdateAppTableRecordRequest = (
        UpdateAppTableRecordRequest.builder()
        .app_token(os.getenv("APP_TOKEN"))
        .table_id(os.getenv("TABLE_ID"))
        .record_id(record_id)
        .request_body(
            AppTableRecord.builder()
            .fields({os.getenv('LARK_FILED'): timestamp_milliseconds})
            .build()
        )
        .build()
    )

    # 发起请求
    option = lark.RequestOption.builder().user_access_token(token).build()
    response: UpdateAppTableRecordResponse = client.bitable.v1.app_table_record.update(
        request, option
    )

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
        )
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()
