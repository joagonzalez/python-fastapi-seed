from os import sys, path
from importlib import import_module

from .logger import loggerConfig
from .default import defaultConfig

from src.utils.cliParser import cliParser

def getSettings(environment: str):
  try:
    sys.path.append(path.abspath('src/config/env'))
    module = import_module(environment)
    return module.config
  except:
    return defaultConfig

settings = getSettings(cliParser.getEnvironment())
