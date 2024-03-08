from email.mime import base
import os
import shutil

from speaksynk_flow_processor.constants.constants import WORKING_DIR

def mapFileNameToUser(fileName):
    first_name, last_name, source_language, target_language, gender, email, uuid  = fileName.split("__")
    return {
        "first_name": first_name,
        "last_name": last_name,
        "source_lan": source_language,
        "target_lan": target_language,
        "gender": gender,
        "email": email,
        "uuid": uuid.split('.')[0]
    }


def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        shutil.rmtree(folder)
        createFolder(folder)


def get_file_path(fileKey):
    baseName = fileKey.split("/")[-1]
    return os.path.join(WORKING_DIR, baseName)
