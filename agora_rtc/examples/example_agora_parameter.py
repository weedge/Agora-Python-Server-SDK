#!env python

#coding=utf-8
import os
from common.path_utils import get_log_path_with_filename 
from common.parse_args import parse_args_example
from observer.connection_observer import ExampleConnectionObserver
from agora.rtc.agora_service import AgoraServiceConfig, AgoraService, RTCConnConfig
from agora.rtc.agora_base import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# run this example
# python agora_rtc/examples/example_agora_parameter.py --appId=xxx --channelId=xxx --userId=xxx
sample_options = parse_args_example()
logger.info(f"app_id: {sample_options.app_id}, channel_id: {sample_options.channel_id}, uid: {sample_options.user_id}")


#---------------1. Init SDK
config = AgoraServiceConfig()
config.appid = sample_options.app_id
config.area_code = AreaCode.AREA_CODE_CN.value | AreaCode.AREA_CODE_JP.value
logger.info(f"config.area_code: {config.area_code}")
config.log_path = get_log_path_with_filename(sample_options.channel_id , os.path.splitext(__file__)[0])

agora_service = AgoraService()
agora_service.initialize(config)

#---------------2. Create Connection
con_config = RTCConnConfig(
    client_role_type=ClientRoleType.CLIENT_ROLE_BROADCASTER,
    channel_profile=ChannelProfileType.CHANNEL_PROFILE_LIVE_BROADCASTING,
)

connection = agora_service.create_rtc_connection(con_config)
conn_observer = ExampleConnectionObserver()
connection.register_observer(conn_observer)
connection.connect(sample_options.token, sample_options.channel_id, sample_options.user_id)

agora_parameter = connection.get_agora_parameter()
logger.info(f"audio_pcm_data_send_mode: {agora_parameter.get_string('audio_pcm_data_send_mode')}")
logger.info(f"ret: {agora_parameter.set_parameters('{\"audio_pcm_data_send_mode\":1}')}")
logger.info(f"audio_pcm_data_send_mode: {agora_parameter.get_string('audio_pcm_data_send_mode')}")

agora_parameter = connection.get_agora_parameter()
logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")
logger.info(f"ret: {agora_parameter.set_parameters('{\"che.audio.aec.enable\":true}')}")
logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")
logger.info(f"ret: {agora_parameter.set_parameters('{\"che.audio.aec.enable\":false}')}")
logger.info(f"che.audio.aec.enable: {agora_parameter.get_string('che.audio.aec.enable')}")

agora_parameter = connection.get_agora_parameter()
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
logger.info(f"ret: {agora_parameter.set_parameters('{\"rtc.enable_nasa2\":1}')}")
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
logger.info(f"ret: {agora_parameter.set_parameters('{\"rtc.enable_nasa2\":0}')}")
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")

agora_parameter = connection.get_agora_parameter()
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
logger.info(f"ret: {agora_parameter.set_bool('rtc.enable_nasa2', 0)}")
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")
logger.info(f"ret: {agora_parameter.set_bool('rtc.enable_nasa2', 1)}")
logger.info(f"rtc.enable_nasa2: {agora_parameter.get_bool('rtc.enable_nasa2')}")

agora_parameter = connection.get_agora_parameter()
logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")
logger.info(f"ret: {agora_parameter.set_bool('rtc.test111', 0)}")
logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")
logger.info(f"ret: {agora_parameter.set_bool('rtc.test111', 1)}")
logger.info(f"rtc.test111: {agora_parameter.get_bool('rtc.test111')}")



connection.unregister_observer()
connection.disconnect()
connection.release()
logger.info("release")
agora_service.release()
logger.info("end")