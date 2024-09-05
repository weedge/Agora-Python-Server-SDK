#coding=utf-8
import os
import sys
from common.path_utils import get_log_path_with_filename 

import time
import ctypes
import datetime
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.rtc_connection import IRTCConnectionObserver
from agora_service.local_user_observer import IRTCLocalUserObserver

from common.parse_args import parse_args_example
# 通过传参将参数传进来
#python python_sdk/examples/example_stream_message_send.py --token=xxx --channelId=xxx --userId=xxx --message="hello agora"
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

class DYSConnectionObserver(IRTCConnectionObserver):
    def __init__(self):
        super(DYSConnectionObserver, self).__init__()

    def on_connected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connected:", agora_rtc_conn, conn_info, reason)

    def on_disconnected(self, agora_rtc_conn, conn_info, reason):
        print("CCC Disconnected:", agora_rtc_conn, conn_info, reason)

    def on_connecting(self, agora_rtc_conn, conn_info, reason):
        print("CCC Connecting:", agora_rtc_conn, conn_info, reason)

    def on_user_joined(self, agora_rtc_conn, user_id):
        print("CCC on_user_joined:", agora_rtc_conn, user_id)


class DYSLocalUserObserver(IRTCLocalUserObserver):
    def __init__(self):
        super(DYSLocalUserObserver, self).__init__()

    def on_stream_message(self, local_user, user_id, stream_id, data, length):
        print("CCC on_stream_message:", user_id, stream_id, data, length)
        return 0

    def on_user_info_updated(self, local_user, user_id, msg, val):
        print("CCC on_user_info_updated:", user_id, msg, val)
        return 0

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])


agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    auto_subscribe_audio=0,
    auto_subscribe_video=0,
    client_role_type=1,
    channel_profile=1,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

local_user = connection.get_local_user()
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)

# connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)
stream_id = connection.create_data_stream(False, False)
stream_id2 = connection.create_data_stream(False, False)
print("stream_id:", stream_id)
for i in range(100):
    msg1 = sample_options.msg + " to data_stream:" +  str(stream_id) + " idx:" +  str(i)
    msg2 = sample_options.msg + " to data_stream:" +  str(stream_id2) + " idx:" +  str(i)
    ret = connection.send_stream_message(stream_id, msg1)
    print(msg1, ret)
    ret = connection.send_stream_message(stream_id2, msg2)
    print(msg2, ret)
    time.sleep(2)

connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")