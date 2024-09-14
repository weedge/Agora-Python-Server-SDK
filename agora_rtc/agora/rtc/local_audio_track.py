import time
import ctypes
from .agora_base import *

# Add these function definitions at the module level
agora_local_audio_track_set_enabled = agora_lib.agora_local_audio_track_set_enabled
agora_local_audio_track_set_enabled.restype = ctypes.c_int
agora_local_audio_track_set_enabled.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_audio_track_is_enabled = agora_lib.agora_local_audio_track_is_enabled
agora_local_audio_track_is_enabled.restype = ctypes.c_int
agora_local_audio_track_is_enabled.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int)]

agora_local_audio_track_get_state = agora_lib.agora_local_audio_track_get_state
agora_local_audio_track_get_state.restype = ctypes.c_int
agora_local_audio_track_get_state.argtypes = [AGORA_HANDLE]

# agora_local_audio_track_get_statistics = agora_lib.agora_local_audio_track_get_statistics
# agora_local_audio_track_get_statistics.restype = ctypes.POINTER(local_audio_track_stats)
# agora_local_audio_track_get_statistics.argtypes = [AGORA_HANDLE]

# agora_local_audio_track_destroy_statistics = agora_lib.agora_local_audio_track_destroy_statistics
# agora_local_audio_track_destroy_statistics.restype = None
# agora_local_audio_track_destroy_statistics.argtypes = [AGORA_HANDLE, ctypes.POINTER(local_audio_track_stats)]

agora_local_audio_track_adjust_publish_volume = agora_lib.agora_local_audio_track_adjust_publish_volume
agora_local_audio_track_adjust_publish_volume.restype = ctypes.c_int
agora_local_audio_track_adjust_publish_volume.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_audio_track_get_publish_volume = agora_lib.agora_local_audio_track_get_publish_volume
agora_local_audio_track_get_publish_volume.restype = ctypes.c_int
agora_local_audio_track_get_publish_volume.argtypes = [AGORA_HANDLE, ctypes.POINTER(ctypes.c_int)]

agora_local_audio_track_enable_local_playback = agora_lib.agora_local_audio_track_enable_local_playback
agora_local_audio_track_enable_local_playback.restype = ctypes.c_int
agora_local_audio_track_enable_local_playback.argtypes = [AGORA_HANDLE, ctypes.c_int]

agora_local_audio_track_enable_ear_monitor = agora_lib.agora_local_audio_track_enable_ear_monitor
agora_local_audio_track_enable_ear_monitor.restype = ctypes.c_int
agora_local_audio_track_enable_ear_monitor.argtypes = [AGORA_HANDLE, ctypes.c_int, ctypes.c_int]

# agora_local_audio_track_set_max_buffer_audio_frame_number = agora_lib.agora_local_audio_track_set_max_bufferd_frame_number
# agora_local_audio_track_set_max_buffer_audio_frame_number.restype = None
# agora_local_audio_track_set_max_buffer_audio_frame_number.argtypes = [AGORA_HANDLE, ctypes.c_int]

# agora_local_audio_track_clear_buffer = agora_lib.agora_local_audio_track_clear_sender_buffer
# agora_local_audio_track_clear_buffer.restype = ctypes.c_int
# agora_local_audio_track_clear_buffer.argtypes = [AGORA_HANDLE]


class LocalAudioTrack:
    def __init__(self, track_handle):
        self.track_handle = track_handle

    def set_enabled(self, enable):
         agora_local_audio_track_set_enabled(self.track_handle, enable)        

    def is_enabled(self):
        enabled = ctypes.c_int()
        ret = agora_local_audio_track_is_enabled(self.track_handle, ctypes.byref(enabled))
        if ret != 0:
            print(f"Failed to get local audio track enabled state, error code: {ret}")
        return ret, enabled.value

    def get_state(self):
        return agora_local_audio_track_get_state(self.track_handle)

    # def get_statistics(self):
    #     stats_ptr = agora_local_audio_track_get_statistics(self.track_handle)
    #     if not stats_ptr:
    #         print("Failed to get local audio track statistics")
    #         return None
    #     stats = stats_ptr.contents
    #     self.destroy_statistics(stats_ptr)
    #     return stats

    # def destroy_statistics(self, stats):
    #     agora_local_audio_track_destroy_statistics(self.track_handle, stats)

    def adjust_publish_volume(self, volume):
        ret = agora_local_audio_track_adjust_publish_volume(self.track_handle, volume)
        if ret != 0:
            print(f"Failed to adjust publish volume, error code: {ret}")
        return ret

    def get_publish_volume(self):
        volume = ctypes.c_int()
        ret = agora_local_audio_track_get_publish_volume(self.track_handle, ctypes.byref(volume))
        if ret != 0:
            print(f"Failed to get publish volume, error code: {ret}")
        return ret, volume.value

    def enable_local_playback(self, enable):
        ret = agora_local_audio_track_enable_local_playback(self.track_handle, enable)
        if ret != 0:
            print(f"Failed to enable local playback, error code: {ret}")
        return ret

    def enable_ear_monitor(self, enable, include_audio_filter):
        ret = agora_local_audio_track_enable_ear_monitor(self.track_handle, enable, include_audio_filter)
        if ret != 0:
            print(f"Failed to enable ear monitor, error code: {ret}")
        return ret

    # def set_max_buffer_audio_frame_number(self, num):
    #     agora_local_audio_track_set_max_buffer_audio_frame_number(self.track_handle, num)

    # def clear_buffer(self):
    #     ret = agora_local_audio_track_clear_buffer(self.track_handle)
    #     if ret != 0:
    #         print(f"Failed to clear buffer, error code: {ret}")
    #     return ret

    def release(self):
        pass
        # if self.track_handle:
        #     agora_local_audio_track_release(self.track_handle)
        #     self.track_handle = None