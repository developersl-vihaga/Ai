import os
from cme.paths import DATA_PATH
def get_script(path):
    with open(os.path.join(DATA_PATH, path), "r") as script:
        return script.read()