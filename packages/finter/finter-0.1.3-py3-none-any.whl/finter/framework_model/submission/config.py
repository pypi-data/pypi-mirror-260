from enum import Enum, auto


class ModelTypeConfig(Enum):
    ALPHA = {"class_name": "Alpha", "file_name": "am.py"}
    PORTFOLIO = {"class_name": "Portfolio", "file_name": "pf.py"}

    @property
    def class_name(self):
        return self.value["class_name"]

    @property
    def file_name(self):
        return self.value["file_name"]

    @classmethod
    def available_options(cls):
        return ", ".join([item.name for item in cls])


class ModelUniverseConfig(Enum):
    KR_STOCK = auto()

    def get_config(self, model_type: ModelTypeConfig):
        if self == ModelUniverseConfig.KR_STOCK:
            return {
                "exchange": "krx",
                "universe": "krx",
                "instrument_type": "stock",
                "freq": "1d",
                "position_type": "target",
                "type": model_type.name.lower(),
                "exposure": "long_only",
            }
        else:
            raise ValueError(f"Unknown universe: {self}")

    @classmethod
    def available_options(cls):
        return ", ".join([item.name for item in cls])
