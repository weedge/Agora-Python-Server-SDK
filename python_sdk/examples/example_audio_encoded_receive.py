#!env python

#coding=utf-8

import time
import os
from common.path_utils import get_log_path_with_filename 
from observer.connection_observer import DYSConnectionObserver
from observer.audio_frame_observer import DYSAudioFrameObserver
from observer.local_user_observer import DYSLocalUserObserver
from agora_service.agora_service import AgoraServiceConfig, AgoraService, AudioSubscriptionOptions, RTCConnConfig
from agora_service.agora_base import *



from common.parse_args import parse_args_example
# 通过传参将参数传进来
##python python_sdk/examples/example_audio_encoded_receive.py --token=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
print("app_id:", sample_options.app_id, "channel_id:", sample_options.channel_id, "uid:", sample_options.user_id)


#---------------1. Init SDK
config = AgoraServiceConfig()
config.enable_audio_processor = 1
config.enable_audio_device = 0
# config.enable_video = 1
config.appid = sample_options.app_id
config.log_path = get_log_path_with_filename(os.path.splitext(__file__)[0])
agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
sub_opt = AudioSubscriptionOptions(
        packet_only = 1,
        pcm_data_only = 0,
        bytes_per_sample = 2,
        number_of_channels = 1,
        sample_rate_hz = 16000
)

con_config = RTCConnConfig(
    auto_subscribe_audio=1,
    auto_subscribe_video=0,
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
    # audio_recv_media_packet = 1,
    # audio_send_media_packet = 1,
    audio_subs_options = sub_opt,
    enable_audio_recording_or_playout = 0,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = DYSConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

#---------------3. Create Media Sender
media_node_factory = agora_service.create_media_node_factory()
audio_sender = media_node_factory.create_audio_encoded_frame_sender()
audio_track = agora_service.create_custom_audio_track_encoded(audio_sender, 0)

local_user = connection.get_local_user()
local_user.set_playback_audio_frame_before_mixing_parameters(1, 48000)
localuser_observer = DYSLocalUserObserver()
local_user.register_local_user_observer(localuser_observer)
audio_frame_observer = DYSAudioFrameObserver()
local_user.register_audio_frame_observer(audio_frame_observer)
# local_user.subscribe_audio("3")
local_user.subscribe_all_audio()

#---------------4. Send Media Stream
# audio_track.set_enabled(1)
# local_user.publish_audio(audio_track)

time.sleep(100)
# local_user.unpublish_audio(audio_track)
# audio_track.set_enabled(0)
connection.unregister_observer()
connection.disconnect()
connection.release()
print("release")
agora_service.release()
print("end")