#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sse_cache.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    sse消息推送和订阅

    :author: Tangshimin
    :copyright: (c) 2024, Tungee
    :date created: 2024-01-29

"""
import json
from datetime import datetime


class SseConnectStatsCache(object):
    """
    节点sse连接状态信息统计缓存
    用于统计每个节点下的所有channel-sse连接状态信息，用于查看节点下所有用户的连接状态
    info : {
        'channel': '122121',
        'connect_time': '2024-01-29 12:00:00',
        'extra': {},
    }
    """
    def __init__(self, redis_client, key_prefix):
        self.redis = redis_client
        self.prefix = key_prefix + ':sse:'
        self.expire = 60 * 60 * 48

    def key(self):
        tail = datetime.now().strftime('%Y%m%d')
        return self.prefix + 'connect_stats_info:' + tail

    def add(self, channel, info):
        info = json.dumps(info)
        self.redis.hset(self.key(), channel, info)
        self.redis.expire(self.key(), self.expire)

    def get(self, channel):
        data = self.redis.hget(self.key(), channel)
        if data is None:
            return {}

        if isinstance(data, bytes):
            data = data.decode('utf-8')

        return json.loads(data)

    def get_all_by_day(self, day):
        day_key = self.prefix + 'connect_stats_info:' + day
        datas = self.redis.hgetall(day_key)
        print({
            'title': '获取连接情况统计数据',
            'key': day_key
        })
        result = {}
        if datas is None:
            return {}

        for channel, info in datas.items():
            if isinstance(channel, bytes):
                channel = channel.decode('utf-8')
            if isinstance(info, bytes):
                result[channel] = json.loads(info.decode('utf-8'))

        return result

    def delete(self, channel):
        self.redis.hdel(self.key(), channel)


class SseEventMessageCache(object):
    """
    sse消息缓存
    """
    def __init__(self, redis_client, key_prefix):
        self.redis = redis_client
        self.prefix = key_prefix + ':sse:'
        self.expire = 60 * 60 * 48

    def pub_key(self):
        tail = datetime.now().strftime('%Y%m%d')
        return self.prefix + 'pub_event_message:' + tail

    def sub_key(self):
        tail = datetime.now().strftime('%Y%m%d')
        return self.prefix + 'sub_event_message:' + tail

    def add_pub_message(self, message):
        message = json.dumps(message)
        self.redis.lpush(self.pub_key(), message)
        self.redis.expire(self.pub_key(), self.expire)

    def add_sub_message(self, message):
        message = json.dumps(message)
        self.redis.lpush(self.sub_key(), message)
        self.redis.expire(self.sub_key(), self.expire)

    def get_pub_all_by_day(self, day):
        day_key = self.prefix + 'pub_event_message:' + day
        print({
            'title': '获取推送消息统计数据',
            'key': day_key
        })
        message = self.redis.lrange(day_key, 0, -1)
        result = list()
        if message is None:
            return []

        for i in range(len(message)):
            if isinstance(message[i], bytes):
                result.append(
                    json.loads(message[i].decode('utf-8'))
                )

        return result

    def get_sub_all_by_day(self, day):
        day_key = self.prefix + 'sub_event_message:' + day
        print({
            'title': '获取接收消息统计数据',
            'key': day_key
        })
        result = list()
        message = self.redis.lrange(day_key, 0, -1)
        if message is None:
            return []

        for i in range(len(message)):
            if isinstance(message[i], bytes):
                result.append(
                    json.loads(message[i].decode('utf-8'))
                )

        return result
