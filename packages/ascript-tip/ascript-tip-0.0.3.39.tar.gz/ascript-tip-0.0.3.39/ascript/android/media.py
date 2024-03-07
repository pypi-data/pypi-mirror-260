
from airscript.system import Media as asMedia
from airscript.system import TTSAliHelper
from airscript.system import AliTTsParam
import  threading
def volume(percent:int,type:int =3):
    asMedia.volume(percent,type)

def talk(msg:str):
    asMedia.talk(msg)

def play(path:str,callback=None):
    if callback:
        asMedia.play(path,callback)
    else:
        asMedia.play(path)

def recode(path:str,time=None):
    if time:
        return asMedia.recode(path,time)
    else:
        return asMedia.recode(path)

def vibrate(time:int=200):
    asMedia.vibrate(time)


ali_tts_lock = threading.Lock()
def ali_tts(config:dict,tts_msg:str,autp_play:bool=True,save_file=None):
    with ali_tts_lock:
        tts =  TTSAliHelper.getInstance()
        tts.init(config['app_key'],config['ak_id'],config['ak_secret'],config['font_name'])
        tts.setPlay(autp_play)
        if save_file:
            tts.saveFile(save_file)

        return tts.change(tts_msg)


class AliTts:
    def __init__(self,app_key:str,ak_id:str,ak_secret:str,font_name:str="siqi",speed_level:str="1",pitch_level:str="0",volume:str="1.0"):
        self.tts_core = TTSAliHelper.getInstance()
        param = AliTTsParam()
        param.setApp_key(app_key)
        param.setAk_id(ak_id)
        param.setAk_secret(ak_secret)
        param.setFont_name(font_name)
        param.setSpeed_level(speed_level)
        param.setPitch_level(pitch_level)
        param.setVolume(volume)
        self.tts_core.init_params(param)

    def start(self,tts_msg:str,auto_play:bool=True,save_file=None):
        self.tts_core.setPlay(auto_play)
        self.tts_core.saveFile(save_file)
        return self.tts_core.change(tts_msg)


