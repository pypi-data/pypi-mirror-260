import json
from enum import Enum
from typing import Dict

HTML_SLOGAN: str = """
<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: 
pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: 
"Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; 
margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p> 
Evan <br/><span style="font-size:30px">锲而舍之，朽木不折；锲而不舍，金石可镂。</span></p></div>
"""

JSON_SLOGAN: str = json.dumps({"message": "WELCOME!!!"})


class ELanguage(Enum):
    ENGLISH = "EN"
    CHINESE = "ZH"


RESPONSE_MESSAGE: Dict[int, Dict[ELanguage, str]] = {
    20000: {
        ELanguage.ENGLISH: "Success",
        ELanguage.CHINESE: "成功",
    },
    20001: {
        ELanguage.ENGLISH: "Success And Do Nothing",
        ELanguage.CHINESE: "成功且无操作",
    },
    20201: {
        ELanguage.ENGLISH: "Accepted",
        ELanguage.CHINESE: "已接受",
    },
    40000: {
        ELanguage.ENGLISH: "Failed",
        ELanguage.CHINESE: "失败",
    },
    40001: {
        ELanguage.ENGLISH: "Bad Request",
        ELanguage.CHINESE: "错误请求",
    },
    40101: {
        ELanguage.ENGLISH: "Unauthorized",
        ELanguage.CHINESE: "未授权",
    },
    40301: {
        ELanguage.ENGLISH: "Forbidden",
        ELanguage.CHINESE: "禁止",
    },
    40302: {
        ELanguage.ENGLISH: "Token Invalid Or Expired",
        ELanguage.CHINESE: "Token 无效或已过期",
    },
    40400: {
        ELanguage.ENGLISH: "Not Found",
        ELanguage.CHINESE: "未找到",
    },
    40402: {
        ELanguage.ENGLISH: "I18n Not Found",
        ELanguage.CHINESE: "I18n 未找到",
    },
    40500: {
        ELanguage.CHINESE: "请求方法不允许",
        ELanguage.ENGLISH: "Method Not Allowed",
    },
    50000: {
        ELanguage.ENGLISH: "Internal Server Error",
        ELanguage.CHINESE: "内部服务器错误",
    },
    50001: {
        ELanguage.ENGLISH: "Database Error",
        ELanguage.CHINESE: "数据库错误",
    },
}
