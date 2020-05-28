from logging import config, getLogger
from toml_config.core import Config

app_config = Config('app.config.toml')

config.fileConfig('logger.config')
logger = getLogger('app')


