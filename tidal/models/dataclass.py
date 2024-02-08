from models import *


class DataClass:
    def __init__(self, data: dict):
        self._set(data)

    def _set(self, data: dict[str,]):
        for k, v in data.items():

            if isinstance(v, dict):
                try:
                    abc_instance = globals[k[0].upper + k[1:]](v)
                    setattr(self, k, abc_instance)
                except Exception:
                    setattr(self, k, v)
            else:
                setattr(self, k, v)
