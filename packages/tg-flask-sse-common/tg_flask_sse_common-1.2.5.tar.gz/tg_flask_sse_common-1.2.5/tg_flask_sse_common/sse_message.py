#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sse_message.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    sse消息格式定义

    :author: Tangshimin
    :copyright: (c) 2024, Tungee
    :date created: 2024-01-29

"""
import json
from datetime import datetime

from .sse_constant import SseClientConfig, SseSystemEventType
from .sse_constant import SseMessageField


class SseMessage(object):
    def __init__(self, channel, data, event=None, _id=None, retry=None):
        self.channel = channel
        self.data = data
        self.event = event
        self.id = _id
        self.retry = retry

    def to_dict(self):
        result = {
            SseMessageField.DATA: self.data,
            SseMessageField.CHANNEL: self.channel
        }
        if self.event:
            result[SseMessageField.EVENT] = self.event
        if self.id:
            result[SseMessageField.ID] = self.id
        if self.retry:
            result[SseMessageField.RETRY] = self.retry
        return result

    def to_rsp_str(self):
        if isinstance(self.data, str):
            data = self.data
        else:
            data = json.dumps(self.data)
        lines = ["%s:%s" % (SseMessageField.DATA, line) for line in data.splitlines()]
        if self.event:
            lines.insert(0, "%s:%s" % (SseMessageField.EVENT, self.event))
        if self.id:
            lines.append("%s:%s" % (SseMessageField.ID, self.id))
        if self.retry:
            lines.append("%s:%s" % (SseMessageField.RETRY, self.retry))
        if self.channel:
            lines.append("%s:%s" % (SseMessageField.CHANNEL, self.channel))
        return "\n".join(lines) + "\n\n"

#
# # redis消息
# REDIS_MESSAGE = SseMessage(
#     channel=SseSystemEventType.REDIS,
#     data=SseSystemEventType.REDIS,
#     event=SseSystemEventType.REDIS,
#     _id=str(int(datetime.now().timestamp() * 1000000)),
#     retry=SseClientConfig.MAX_CONNECT_TIME * 1000
# )
#
# # error消息
# ERROR_MESSAGE = SseMessage(
#     channel=SseSystemEventType.ERROR,
#     data=SseSystemEventType.ERROR,
#     event=SseSystemEventType.ERROR,
#     _id=str(int(datetime.now().timestamp() * 1000000)),
#     retry=SseClientConfig.MAX_CONNECT_TIME * 1000
# )
#
# # end消息
# END_MESSAGE = SseMessage(
#     channel=SseSystemEventType.END,
#     data=SseSystemEventType.END,
#     event=SseSystemEventType.END,
#     _id=str(int(datetime.now().timestamp() * 1000000)),
#     retry=SseClientConfig.MAX_CONNECT_TIME * 1000
# )
#
# # connect消息
# CONNECT_MESSAGE = SseMessage(
#     channel=SseSystemEventType.CONNECT,
#     data=SseSystemEventType.CONNECT,
#     event=SseSystemEventType.CONNECT,
#     _id=str(int(datetime.now().timestamp() * 1000000)),
#     retry=SseClientConfig.MAX_CONNECT_TIME * 1000
# )