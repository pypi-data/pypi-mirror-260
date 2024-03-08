import json
import os
from typing import Callable

from speaksynk_flow_processor.constants.constants import WORKING_DIR
from speaksynk_flow_processor.utils.utils import get_file_path


class HandleProcessData:
    def __init__(
        self,
        _identifier: str,
        download: Callable[[str], None],
        upload: Callable[[str, str], None],
        check_file: Callable[[str], tuple[bool, any]],
        folder: str = "process_data",
    ) -> None:
        self.identifier = _identifier
        self.pd = f"{folder}/{self.identifier}.json"
        self.data: dict | None = None
        self._download = download
        self._upload = upload
        self._check_file = check_file
        self._updated = False

    def __enter__(self):
        print(f"PD :{self.pd})")
        [success, _] = self._check_file(self.pd)
        if success:
            print(f"SUCCESS")
            self._download(self.pd)
            self.load()
        else:
            print(f"FAIL")
            self.data = {}
        return self

    def set_attributes(self, newKeyValues: dict):
        self.data.update(newKeyValues)
        self._updated = True

    def get_attribute(self, key: str, reload=False):
        if not self.data or reload:
            self.load()

        return self.data.get(key)

    def load(self):
        with open(os.path.join(WORKING_DIR, self.pd), "r") as jsonFile:
            print("loading...")
            self.data = json.load(jsonFile)
            print(f"DATA : {self.data}")
            return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._updated:
            with open(get_file_path(self.pd), "w") as jsonFile:
                json.dump(self.data, jsonFile)

            self._upload(self.pd, self.pd)
