#!env python

#coding=utf-8

import time
import ctypes
from agora_service.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora_service.rtc_connection import *
from agora_service.media_node_factory import *
from agora_service.audio_pcm_data_sender import *
from agora_service.audio_frame_observer import *
from agora_service.media_node_factory import *

# conn_observer callback
def on_connected(agora_rtc_conn, conn_info, reason):
    print("Connected:", agora_rtc_conn, conn_info, reason)

def on_disconnected(agora_rtc_conn, conn_info, reason):
    print("Disconnected:", agora_rtc_conn, conn_info, reason)

def on_connecting(agora_rtc_conn, conn_info, reason):
    print("Connecting:", agora_rtc_conn, conn_info, reason)

def on_user_joined(agora_rtc_conn, user_id):
    print("on_user_joined:", agora_rtc_conn, user_id)

# def on_get_playback_audio_frame_param(agora_local_user):
#     audio_params_instance = AudioParams()
#     return audio_params_instance

def on_playback_audio_frame_before_mixing(agora_local_user, channelId, uid, frame):
    print("on_playback_audio_frame_before_mixing")#, channelId, uid)
    return 0

def on_record_audio_frame(agora_local_user ,channelId, frame):
    print("on_record_audio_frame")
    return 0

def on_playback_audio_frame(agora_local_user, channelId, frame):
    print("on_playback_audio_frame")
    return 0

def on_mixed_audio_frame(agora_local_user, channelId, frame):
    print("on_mixed_audio_frame")
    return 0

def on_ear_monitoring_audio_frame(agora_local_user, frame):
    print("on_ear_monitoring_audio_frame")
    return 0

def on_playback_audio_frame_before_mixing(agora_local_user, channelId, uid, frame):
    print("on_playback_audio_frame_before_mixing")
    return 0

def on_get_audio_frame_position(agora_local_user):
    print("on_get_audio_frame_position")
    return 0

#c api def
# AGORA_HANDLE agora_local_user, user_id_t user_id, int stream_id, const char* data, size_t length
#user_id: string type; steream_id: int, data: byte, lenght: int
def on_stream_message(local_user, user_id, stream_id, data, length):
    print("on_stream_message:", user_id, stream_id, data, length)
    #print("on_stream_message: userid is {user_id}, streamid is {stream_id}, data is {data}, length is {length }")
    return 0

#void (*on_user_info_updated)(AGORA_HANDLE agora_local_user, user_id_t user_id, int msg, int val);
#user_id: string type; msg: int, val: int
def on_user_info_updated(local_user, user_id, msg, val):
    print("on_user_info_updated:", user_id, msg, val)
    #print("on_user_info_updated: userid is: {user_id}, msg is: {msg}, val is: {val}")
    return 0

#pacer class
class Pacer:
    def __init__(self,interval):
        self.last_call_time = time.time()
        self.interval = interval

    def pace(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < self.interval:
            time.sleep(self.interval - elapsed_time)
            print("sleep time:", (self.interval - elapsed_time)*1000)
        self.last_call_time = time.time()


example_dir = os.path.dirname(os.path.abspath(__file__))
pcm_file_path = os.path.join(example_dir, 'demo.pcm')


# 通过传参将参数传进来
# 例如： python examples/example_send_pcm.py {appid} {token} {channel_id} ./test_data/demo.pcm {userid}
appid = sys.argv[1]
token = sys.argv[2]
channel_id = sys.argv[3]
pcm_file_path = sys.argv[4]
# check argv len
if len(sys.argv) > 5:
    uid = sys.argv[5]
else:
    uid = "0"
print("appid:", appid, "token:", token, "channel_id:", channel_id, "pcm_file_path:", pcm_file_path, "uid:", uid)

#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = appid
config.log_path = os.path.join(example_dir, 'agorasdk.log')

agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    auto_subscribe_audio=1,
    auto_subscribe_video=0,
    client_role_type=1,
    channel_profile=1,
)
pcm_observer = AudioFrameObserver(
    on_record_audio_frame=ON_RECORD_AUDIO_FRAME_CALLBACK(on_record_audio_frame),
    on_playback_audio_frame=ON_PLAYBACK_AUDIO_FRAME_CALLBACK(on_playback_audio_frame),
    on_ear_monitoring_audio_frame=ON_EAR_MONITORING_AUDIO_FRAME_CALLBACK(on_ear_monitoring_audio_frame),
    on_playback_audio_frame_before_mixing=ON_PLAYBACK_AUDIO_FRAME_BEFORE_MIXING_CALLBACK(on_playback_audio_frame_before_mixing),
    on_get_audio_frame_position=ON_GET_AUDIO_FRAME_POSITION_CALLBACK(on_get_audio_frame_position),
)
con_config.pcm_observer = pcm_observer
connection = agora_service.create_rtc_connection(con_config)

conn_observer = RTCConnectionObserver(
    on_connected=ON_CONNECTED_CALLBACK(on_connected),
    on_disconnected=ON_CONNECTED_CALLBACK(on_disconnected),
    on_user_joined=ON_USER_JOINED_CALLBACK(on_user_joined)
)

localuser_observer = RTCLocalUserObserver( 
    on_stream_message=ON_STREAM_MESSAGE_CALLBACK(on_stream_message),
    on_user_info_updated=ON_USER_INFO_UPDATED_CALLBACK(on_user_info_updated)
)
connection.register_observer(conn_observer)
connection.connect(token, channel_id, uid)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
audio_track_pcm = agora_service.create_custom_audio_track(pcm_data_sender)
local_user = connection.get_local_user()
audio_track_pcm.set_max_buffer_audio_frame_number(320*2000)

#---------------4. Send Media Stream
audio_track_pcm.set_enabled(1)
local_user.publish_audio(audio_track_pcm)

sendinterval = 0.1
Pacer = Pacer(sendinterval)
count = 0
packnum = int((sendinterval*1000)/10)
with open(pcm_file_path, "rb") as file:

    while True:
        if count < 10:
            packnum = 100
        frame_buf = bytearray(320*packnum)            
        success = file.readinto(frame_buf)
        if not success:
            break
        frame = PcmAudioFrame()
        frame.data = frame_buf
        frame.timestamp = 0
        frame.samples_per_channel = 160*packnum
        frame.bytes_per_sample = 2
        frame.number_of_channels = 1
        frame.sample_rate = 16000

        ret = pcm_data_sender.send(frame)
        count += 1
        print("count,ret=",count, ret)
        Pacer.pace()
           
#---------------5. Stop Media Sender And Release
time.sleep(10)
audio_track_pcm.set_enabled(0)
local_user.unpublish_audio(audio_track_pcm)

connection.disconnect()
# connection.Release()
print("release")
agora_service.release()
print("end")