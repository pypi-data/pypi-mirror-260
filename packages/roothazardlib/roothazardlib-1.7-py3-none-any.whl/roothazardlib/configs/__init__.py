"""
Here we have frequently used config models for TLS clients
and general servers. Also, we have const singleton yaml
config which can work with classes inherited from ConfigModel
"""

from .secure_client_service import TLSConfigModel, ServerConfigModel
from .yaml_config_singletone import ConfigModel, YamlConfig, ConstModel
