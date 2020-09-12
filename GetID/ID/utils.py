from enum import Enum


class response_msg(Enum):
    MSG_ERROR = "请正确填写信息"
    MSG_NOT_FOUND = "没有查到你的信息"
    MSG_SYSTEM_ERROR = "系统错误请联系客服"
