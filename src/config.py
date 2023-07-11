from attr import dataclass

import yaml

from typing import Any, Dict, List, Optional

@dataclass
class ObjectConfig:
    NAME: str
    DATASET_FOLDER: str
    MIN_AREA: int
    MAX_AREA: int
    CLIP_WIDTH: int
    CLIP_HEIGHT: int
    ALLOWED_IOU: float
    DETECTION_THRESHOLD: float
    TF_MODEL_PATH: str

    CLIP_STRATEGY: Optional[str] = None
    CONVEYOR_DIRECTION: Optional[int] = None
    CONVEYOR_SPEED: Optional[int] = None

    HAS_CAPTURE_FRAME: Optional[bool] = False
    CAPTURE_FRAME_X: Optional[int] = None
    CAPTURE_FRAME_Y: Optional[int] = None
    CAPTURE_FRAME_WIDTH: Optional[int] = None
    CAPTURE_FRAME_HEIGHT: Optional[int] = None


class DependencyManager:
    config = None

    @staticmethod
    def set_config(config):
        DependencyManager.config = config

    @staticmethod
    def get_config():
        return DependencyManager.config

class Config:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)
        self.object_configs = None
        self._load_params()

    def _load_config(self, config_file):
        """
        Load the configuration from a YAML file.

        Parameters:
            config_file (str): The path to the YAML configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        
        return config

    def _load_params(self):
        """
        Load the configuration parameters as attributes using metaprogramming.
        """
        for key, value in self.config.items():
            setattr(self, key, value)

    def get_objects(self) -> List[ObjectConfig]:
        if not self.object_configs:
            self.object_configs = [ObjectConfig(**object_dict) for object_dict in self.config.get('OBJECTS', [])]
        
        return self.object_configs
