#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kimi_types
# @Time         : 2024/2/29 16:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


class KimiData(BaseModel):
    """
    {"error":{"error_type":"openai.completion.stream","message":"Kimi 现在有点累了，晚一点再来问问我吧！","detail":"runtime error: invalid memory address or nil pointer dereference"},"event":"error"}

    data: {"content":"1+1","event":"req","group_id":"cljdett0tc12f8jcpc7g","id":"cljdett0tc12f8jcpc8g","refs":[]}
    data: {"event":"resp","group_id":"cljdett0tc12f8jcpc7g","id":"cljdett0tc12f8jcpc90"}
    data: {"event":"debug","message":{"need2search":false,"search_target":"","search_language":""}}
    data: {"event":"debug","message":{"need2search":true,"search_target":"南京今天天气","search_language":"zh-cn"}}
    data: {"event":"search_plus","msg":{"type":"start"}}
    data: {"event":"search_plus","msg":{"successNum":1,"title":"南京天气","type":"get_res","url":"http://m.nmc.cn/publish/forecast/AJS/nanjing.html"}}
        {'successNum': 1, 'title': '南京天气预报25天|南京未来25天天气|南京天气预报未来25天...', 'type': 'get_res', 'url': 'http://www.tqw1.com/jsnanjing_25.shtml'}
    data: {"event":"cmpl","text":" "}
    data: {"event":"cmpl","text":"1"}
    data: {"event":"cmpl","text":"å "}
    data: {"event":"done"}
    data: {"event":"cmpl","text":"1"}
    data: {"event":"cmpl","text":"ç­"}
    data: {"event":"cmpl","text":"äº"}
    data: {"event":"cmpl","text":"2"}
    data: {"event":"cmpl","text":"ã"}
    data: {"event":"all_done"}


    """
    event: str = 'cmpl'  # 事件类型

    prompt: str = Field(default='', alias='content')
    content: str = Field(default='', alias='text')  # 生成的文本

    # id: Optional[str] = None
    # group_id: Optional[str] = None

    msg: dict = {}
    refs: Optional[List[str]] = None  # 文件问答

    # {"error_type":"auth.token.invalid","message":"您的授权已过期，请重新登录"}
    # {"error_type":"chat.forbidden","message":"此会话已被禁用"}
    error_type: Optional[str] = None
    message: Optional[Any] = None
