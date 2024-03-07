#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sse_core.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    sse消息推送和订阅逻辑

    :author: Tangshimin
    :copyright: (c) 2024, Tungee
    :date created: 2024-01-29

"""
import threading
import redis
from datetime import datetime

from .sse_constant import RedisConfig, SseSystemEventType, SseClientConfig
from .sse_clients import SseClients
from .sse_redis_pub_sub import SseRedisPubSub


class Sse(object):
    def __init__(self, redis_config, sse_clients_config):
        host = redis_config['host'] or RedisConfig.HOST
        port = redis_config['port'] or RedisConfig.PORT
        password = redis_config['password'] or RedisConfig.PASSWORD
        db = redis_config['db'] or RedisConfig.DB
        key_prefix = redis_config['key_prefix'] or RedisConfig.KEY_PREFIX

        # 初始化redis连接
        redis_client = redis.StrictRedis(
            host=host, port=port,
            password=password, db=db,
        )
        self.redis_client = redis_client

        # 初始化sse连接对象
        sse_clients = SseClients(
            sse_clients_config=sse_clients_config
        )
        self.sse_clients = sse_clients

        # 初始化redis-pub-sub对象
        self.sse_redis_pub_sub = SseRedisPubSub(
            redis_client=redis_client, key_prefix=key_prefix,
            sse_clients=sse_clients
        )

    def connect(self, channel, extra=None):
        """
        添加连接对象, 并订阅sse消息, 添加信息到redis订阅频道
        订阅后，推送一条带节点ip地址的消息，通知非当前ip地址节点的连接进行断开
        :param channel: 频道id
        :param extra: 额外信息
        """
        ok, msg = self.sse_clients.connect(channel)

        self.sse_redis_pub_sub.subscribe_channel(channel=channel, extra=extra)

        self.sse_redis_pub_sub.publish_message(
            channel=channel,
            data={
                'msg': 'connect success',
                'ln_id': self.sse_clients.get_local_node_id()
            },
            event=SseSystemEventType.CONNECT,
            _id=str(int(datetime.now().timestamp() * 1000000)),
            retry=SseClientConfig.MAX_CONNECT_TIME * 1000
        )

        return ok, msg

    def listen(self):
        """
        开启sse消息监听redis-频道，服务启动时调用
        """
        if not self.sse_clients.is_running:
            self.sse_clients.is_running = True
            self.sse_redis_pub_sub.listen()

    def listen_message(self, channel):
        """
        监听内存消息队列
        """
        message_generator = self.sse_clients.listen_message(channel)
        if not message_generator:
            self.sse_redis_pub_sub.disconnect(channel)

        return message_generator

    def publish_business_message(self, channel, event, data, _id=None, retry=None):
        """
        推送sse业务消息, 添加信息到redis频道
        """
        if event in [
            SseSystemEventType.END, SseSystemEventType.ERROR,
            SseSystemEventType.REDIS, SseSystemEventType.CONNECT
        ]:
            print("business event type error, can not use system event type")
            return 0

        return self.sse_redis_pub_sub.publish_message(
            channel=channel,
            data=data,
            event=event,
            _id=_id,
            retry=retry
        )

    def publish_end_message(self, channel):
        """
        推送sse-end系统消息, 添加信息到redis频道
        """
        return self.sse_redis_pub_sub.publish_message(
            channel=channel,
            data=SseSystemEventType.END,
            event=SseSystemEventType.END,
            _id=str(int(datetime.now().timestamp() * 1000000)),
            retry=SseClientConfig.MAX_CONNECT_TIME * 1000
        )

    def sse_run(self):
        """
        开启后台线程监听sse消息，服务启动时调用
        """
        thread = threading.Thread(target=self.listen)
        thread.start()

    def sse_stop(self):
        """
        停止后台sse消息监听线程，服务停止时调用
        """
        self.sse_clients.is_running = False
        return self.sse_redis_pub_sub.disconnect_all()

    def get_stat(self, stat_type, day):
        """
        获取相对应的统计数据
        """
        if stat_type == 'connect':
            return self.sse_redis_pub_sub.get_connect_stat(day)
        elif stat_type == 'pub_message':
            return self.sse_redis_pub_sub.get_pub_message_stat(day)
        elif stat_type == 'sub_message':
            return self.sse_redis_pub_sub.get_sub_message_stat(day)
        else:
            return []

