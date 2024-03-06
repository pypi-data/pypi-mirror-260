# -*- coding: utf-8 -*-
import os
import copy
import json
import logging
from typing import Dict, List
from collections import OrderedDict

import yaml

class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class ConfigManager(metaclass=Singleton):

    def __init__(self):
        self._data_dir = None
        self._config = None

    def init_config(self, data_dir):
        self._data_dir = data_dir
        config_path = os.path.join(data_dir, "config", "service.yaml")
        self._config = yaml.load(
            open(config_path), Loader=yaml.FullLoader)
        logging.info("init config from: %s", config_path)
        
    @property
    def conf_dir(self) -> str:
        return os.path.join(self._data_dir, "config")
        
    @property
    def hdmap_lib_conf_path(self) -> str:
        return os.path.join(self.conf_dir, "hdmap_lib_conf", "hdmap_lib.conf")
      
    @staticmethod
    def _read_conf_file(conf_map: Dict[str, str], conf_file_content: str):
        lines = conf_file_content.splitlines()
        for line in lines:
            param_pair = line.strip().split("=")
            if not param_pair:
                continue
            if len(param_pair) == 1:
                conf_map[param_pair[0]] = None
            else:
                conf_map[param_pair[0]] = param_pair[1]
    
    def _get_runtime_flags(self):
        conf_map = {}
        hdmap_lib_conf = open(self.hdmap_lib_conf_path, "r").read()
        self._read_conf_file(conf_map, hdmap_lib_conf)

        if "--hdmap_lib_config_root" in conf_map:
            conf_map["--hdmap_lib_config_root"] = os.path.join(
                os.path.dirname(self.hdmap_lib_conf_path),
                conf_map["--hdmap_lib_config_root"])
        if "--driverless_road_link_config_path" in conf_map:
            conf_map["--driverless_road_link_config_path"] = os.path.join(
                os.path.dirname(self.hdmap_lib_conf_path),
                conf_map["--driverless_road_link_config_path"])
        if "--yongzhou_road_link_config_path" in conf_map:
            conf_map["--yongzhou_road_link_config_path"] = os.path.join(
                os.path.dirname(self.hdmap_lib_conf_path),
                conf_map["--yongzhou_road_link_config_path"])

        runtime_flags = "\n".join(
            [f"{k}={v}" if v is not None else f"{k}" for k, v in conf_map.items()])
        return runtime_flags



