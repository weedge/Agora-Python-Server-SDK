#!env python

import time
import os
import threading
from common.path_utils import get_log_path_with_filename 
from common.pacer import Pacer
from common.parse_args import parse_args_example
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora_service.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora_service.audio_pcm_data_sender import PcmAudioFrame
from agora_service.agora_base import *
from agora_service.video_frame_sender import ExternalVideoFrame

# 通过传参将参数传进来
#python python_sdk/examples/example_send_pcm_yuv_loop_connection_create_destroy.py --appId=xxx --channelId=xxx --userId=xxx --audioFile=./test_data/demo.pcm --videoFile=./test_data/103_RaceHorses_416x240p30_300.yuv
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)

count = 0
packnum = 0

#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)
def create_conn_and_send(channel_id, uid = 0):
    global count
    global packnum

    #---------------2. Create Connection
    con_config = RTCConnConfig(
        client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
        channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    )
    connection = agora_service.create_rtc_connection(con_config)
    conn_observer = DYSConnectionObserver()
    connection.register_observer(conn_observer)
    connection.connect(sample_options.token, channel_id, uid)

    #---------------3. Create Media Sender
    media_node_factory = agora_service.create_media_node_factory()

    pcm_data_sender = media_node_factory.create_audio_pcm_data_sender()
    audio_track = agora_service.create_custom_audio_track_pcm(pcm_data_sender)
    audio_track.set_max_buffer_audio_frame_number(320*2000)
    
    video_sender = media_node_factory.create_video_frame_sender()
    video_track = agora_service.create_custom_video_track_frame(video_sender)

    local_user = connection.get_local_user()
    localuser_observer = DYSLocalUserObserver()
    local_user.register_local_user_observer(localuser_observer)

    #---------------4. Send Media Stream
    audio_track.set_enabled(1)
    local_user.publish_audio(audio_track)

    video_track.set_enabled(1)
    local_user.publish_video(video_track)

    sendinterval = 0.1
    pacer = Pacer(sendinterval)
    count = 0
    samples = 10

    running = True
    def push_pcm_data_from_file(audio_file):
        global count
        global running
        # if count < 10:
        #     packnum = 100
        frame_buf = bytearray(int(32000*sendinterval))
        success = audio_file.readinto(frame_buf)
        if not success:
            running = False
            return
        frame = PcmAudioFrame()
        frame.data = frame_buf
        frame.timestamp = 0
        frame.samples_per_channel = int(16000*sendinterval)
        frame.bytes_per_sample = 2
        frame.number_of_channels = 1
        frame.sample_rate = 16000
        ret = pcm_data_sender.send_audio_pcm_data(frame)
        count += 1
        print("send pcm: count,ret=",count, ret)
        # pacer.pace()

    width = sample_options.width
    height = sample_options.height
    fps = sample_options.fps
    yuv_len = int(width*height*3/2)
    frame_buf = bytearray(yuv_len)
    def push_video_data_from_file(video_file):
        global running
        global count
        success = video_file.readinto(frame_buf)
        if not success:
            running = False
            return
        frame = ExternalVideoFrame()
        frame.buffer = frame_buf
        frame.type = 1
        frame.format = 1
        frame.stride = width
        frame.height = height
        frame.timestamp = 0
        frame.metadata = "hello metadata"
        ret = video_sender.send_video_frame(frame)        
        count += 1
        print("send yuv: count,ret=",count, ret)
        # pacer.pace()


    def send_test():
        global count
        global packnum
        with open(sample_options.audio_file, "rb") as audio_file, open(sample_options.video_file, "rb") as video_file:
            while running:
                push_pcm_data_from_file(audio_file)
                push_video_data_from_file(video_file)
                time.sleep(0.01)

    send_test()

    local_user.unpublish_audio(audio_track)
    audio_track.set_enabled(0)
    connection.unregister_observer()
    connection.disconnect()
    connection.release()
    print("release")
    


# while True:
#     run_test()


threads = []
for i in range(int(sample_options.channel_number)):
    print("channel", i)
    channel_id = sample_options.channel_id + str(i+1)

    thread = threading.Thread(target=create_conn_and_send, args=(channel_id, sample_options.user_id))
    thread.start()
    threads.append(thread)

    
for t in threads:
    t.join()

agora_service.release()
print("end")