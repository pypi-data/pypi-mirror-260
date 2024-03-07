#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sse_clients.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    sse全局连接对象

    :author: Tangshimin
    :copyright: (c) 2024, Tungee
    :date created: 2024-01-29

"""
from datetime import datetime
import time

from .sse_constant import SseClientConfig, SseSystemEventType
from .sse_message import SseMessageField


class SseClients(object):
    """
    用于全局保存sse连接对象
    背景 : 因为在每个sse长连接中，每次创建redis-pub-sub监听会耗cpu的操作，所以redis-pub-sub需要全局创建，
          如果全局创建redis-pub-sub，就无法区分不同的sse连接，也就无法对不同的sse连接进行操作，
          所以需要一个全局保存sse连接对象的地方
    原理 : 原理类似websocket的全局socket对象机制，每个连接都保存在了全局socket对象中，通过socket_id进行访问
          主要考虑连接建立时，连接断开时，连接异常时的处理，同时提供定时任务清理无效连接
    连接建立 : 保存连接对象
    连接断开 : 删除连接对象
    连接异常 : 删除连接对象
    """

    class Field(object):
        """
        sse全局连接对象字段
        """
        MESSAGE_LIST = 'message_list'
        CONNECT_TIME = 'connect_time'
        LATER_RELEASE = 'later_release'

    class Rsp(object):
        TIMEOUT_CONNECT = 'timeout_connect'     # 超时连接
        END_CONNECT = 'end_connect'             # 主动结束连接
        REPEAT_CONNECT = 'repeat_connect'       # 单个节点重复连接
        D_REPEAT_CONNECT = 'distribute_repeat_connect'     # 分布式其他节点重复连接

    def __init__(self, sse_clients_config):
        self.is_running = False
        self.sse_global_clients = {}

        # 控制连接最大时间，超过时间超过定时任务清理
        max_connect_time = sse_clients_config['max_connect_time'] or SseClientConfig.MAX_CONNECT_TIME
        max_connect_count = sse_clients_config['max_connect_count'] or SseClientConfig.MAX_CONNECT_COUNT
        listen_interval = sse_clients_config['listen_interval'] or SseClientConfig.LISTEN_INTERVAL
        local_node_id = sse_clients_config['local_node_id'] or SseClientConfig.LOCAL_NODE_ID

        self.max_connect_time = max_connect_time
        self.max_connect_count = max_connect_count
        self.listen_interval = listen_interval
        self.local_node_id = local_node_id

    def get_local_node_id(self):
        return self.local_node_id

    def count(self):
        return len(self.sse_global_clients.keys())

    def connect(self, channel):
        """
        添加连接对象，请求建立sse连接时调用
        :param channel: 连接id
        """
        if not channel:
            return False, "channel is empty"

        if len(self.sse_global_clients) > self.max_connect_count:
            return False, "connect count is max"

        channel = str(channel)

        sse_connect_list = self.sse_global_clients.get(channel)
        if not sse_connect_list:
            sse_connect_list = list()

        # 将之前的连接全部设置稍后关闭
        for sse_connect in sse_connect_list:
            sse_connect.update({
                self.Field.LATER_RELEASE: True
            })

        sse_connect_list.append({
            self.Field.MESSAGE_LIST: [],
            self.Field.CONNECT_TIME: datetime.now(),
            self.Field.LATER_RELEASE: False
        })

        self.sse_global_clients.setdefault(channel, sse_connect_list)

        return True, "ok"

    def get_sse(self, channel):
        """
        获取连接对象
        :param channel: 连接id
        """
        sse_connect_list = self.sse_global_clients.get(channel)

        if not sse_connect_list:
            sse_connect_list = []

        return sse_connect_list

    def del_sse(self, channel):
        """
        删除连接对象
        :param channel: 连接id
        """
        if channel in self.sse_global_clients:
            sse_connect_list = self.sse_global_clients.pop(channel)
            for sse_connect in sse_connect_list:
                sse_connect.update({
                    self.Field.LATER_RELEASE: True
                })

    def del_all(self):
        """
        清理所有连接对象
        """
        self.sse_global_clients.clear()

    def add_message(self, channel, message):
        """
        添加消息到连接对象，监听到redis-pub-sub消息时调用
        :param channel: 连接id
        :param message: 消息
        """
        sse_connect_list = self.get_sse(channel)
        for sse_connect in sse_connect_list:
            if not sse_connect:
                continue

            message_list = sse_connect.get(self.Field.MESSAGE_LIST, [])
            message_list.append(message)
            sse_connect.update({
                self.Field.MESSAGE_LIST: message_list,
            })

        self.sse_global_clients.setdefault(channel, sse_connect_list)

    def listen_message(self, channel):
        """
        监听消息
        """
        latest_sse_connect = None
        sse_connect_list = self.get_sse(channel)
        for sse_connect in sse_connect_list:
            if not sse_connect:
                continue
            if sse_connect.get(self.Field.LATER_RELEASE):
                continue

            latest_sse_connect = sse_connect
            break

        if not latest_sse_connect:
            print({
                'title': '当前连接全部等待关闭中，请重新连接',
                'channel': channel,
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
            yield None

        message_list = latest_sse_connect.get(self.Field.MESSAGE_LIST, [])
        connect_time = latest_sse_connect.get(self.Field.CONNECT_TIME, datetime.now())

        run_rsp = self.Rsp.TIMEOUT_CONNECT
        # 最大超时范围内，轮训消息
        while (datetime.now() - connect_time).seconds < self.max_connect_time:
            if latest_sse_connect.get(self.Field.LATER_RELEASE):
                run_rsp = self.Rsp.REPEAT_CONNECT
                break

            if not message_list:
                time.sleep(self.listen_interval)
                continue

            message = message_list.pop(0)
            if not message:
                time.sleep(self.listen_interval)
                continue

            message_dict = message.to_dict()
            event = message_dict.get(SseMessageField.EVENT, '')

            if event == SseSystemEventType.END:
                run_rsp = self.Rsp.END_CONNECT
                break

            if event == SseSystemEventType.CONNECT:
                data = message_dict.get(SseMessageField.DATA, {})
                if data and isinstance(data, dict):
                    local_node_id = data.get('ln_id', '')
                    if local_node_id == self.local_node_id:
                        run_rsp = self.Rsp.D_REPEAT_CONNECT
                        break

            yield message
            time.sleep(self.listen_interval)

        # 移除需要关闭的连接
        for index, sse_connect in enumerate(sse_connect_list):
            if sse_connect.get(self.Field.LATER_RELEASE):
                sse_connect_list.pop(index)

        if run_rsp == self.Rsp.TIMEOUT_CONNECT:
            print({
                'title': '连接超时，关闭轮训',
                'channel': channel,
                'connect_time': datetime.strftime(connect_time, '%Y-%m-%d %H:%M:%S'),
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
        elif run_rsp == self.Rsp.REPEAT_CONNECT:
            print({
                'title': '收到同一节点重复channel连接，关闭轮训',
                'channel': channel,
                'connect_time': datetime.strftime(connect_time, '%Y-%m-%d %H:%M:%S'),
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
        elif run_rsp == self.Rsp.D_REPEAT_CONNECT:
            print({
                'title': '收到其他节点重复channel连接，关闭轮训',
                'channel': channel,
                'connect_time': datetime.strftime(connect_time, '%Y-%m-%d %H:%M:%S'),
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
        elif run_rsp == self.Rsp.END_CONNECT:
            print({
                'title': '收到结束消息，关闭轮训',
                'channel': channel,
                'connect_time': datetime.strftime(connect_time, '%Y-%m-%d %H:%M:%S'),
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
        else:
            print({
                'title': '未知情况，关闭轮训',
                'channel': channel,
                'connect_time': datetime.strftime(connect_time, '%Y-%m-%d %H:%M:%S'),
                'channel_count': len(sse_connect_list),
                'total_channel_count': len(self.sse_global_clients.keys())
            })
        yield None

