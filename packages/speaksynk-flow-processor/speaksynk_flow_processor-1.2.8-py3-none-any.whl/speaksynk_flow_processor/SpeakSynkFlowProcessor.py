import os
import time
from datetime import datetime

from speaksynk_flow_processor.interfaces.IFlow import IFlow
from speaksynk_flow_processor.interfaces.IProcessor import IProcessor
from speaksynk_flow_processor.constants.constants import FILE_NAME_ENVIROMENT_NAME, TRACK_DATA_ENABLED
from speaksynk_flow_processor.track.track import track_method
from speaksynk_flow_processor.utils.utils import mapFileNameToUser
from speaksynk_flow_processor.utils.logger import logger


class SpeakSynkFlowProcessor(IFlow, IProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._file_name = os.environ[FILE_NAME_ENVIROMENT_NAME]
        self._user = mapFileNameToUser(self._file_name)
        self._logger = logger
        self._extension = self._file_name.split(".")[-1]
        self._identifier = os.environ[FILE_NAME_ENVIROMENT_NAME].replace(f".{self._extension}", "")
        self._file_path = None
        self.track_data = {
            "methods": {
                'M': {}
            },
            "filename": {
                "S": self._identifier
            }
        }
        self.is_track_data_enabled =  os.environ[TRACK_DATA_ENABLED] == 'TRUE' if TRACK_DATA_ENABLED in os.environ else False

    @track_method
    def download(self, filekey):
        self._logger.debug("Executing Download Method")
        return super().download(filekey)

    @track_method
    def run(self):
        self._logger.debug("Executing Run Method")
        self.track_data['start_time'] = {
            "N": f"{time.time()}"
        }
        return super().run()

    @track_method
    def upload(self, filekey, fileName):
        self._logger.debug("Executing Upload Method")
        return super().upload(filekey, fileName)
    

    def uploadStats(self):
        return super().uploadStats()
    
    def close(self):
        super().close()
        self._logger.info(f"About to finish step {__class__.__name__}")
        self.track_data['end_time'] = {
            "N": f"{time.time()}"
        }
        if self.is_track_data_enabled:
            self.uploadStats()

    
    def log_time(self, identifier, module_name, end=False):
        current_dnt = datetime.now()
        pos = "Finshed" if end else "Started"
        self._logger.info(f"{module_name},{identifier},{pos},{current_dnt}")
        
    def getTrackData(self):
        return self.track_data
    