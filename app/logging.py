import json
import os
from typing import Optional

from app.configs.settings import ROOT_DIR


def logging_config() -> Optional[json]:
    file_path = os.path.join(ROOT_DIR, 'logging', 'logging.json')
    if not file_path:
        print('Logging Config file path do not exit')
        return None
    try:
        with open(file_path) as fd:
            content = fd.read()
            return json.loads(content)
    except Exception:
        print('Logging Config Error')
        return None
